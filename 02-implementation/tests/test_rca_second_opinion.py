"""Tests for the multi-vendor model registry in rca_second_opinion.py.

No real network calls and no real API key required anywhere here: requests.post
is always mocked, and GEMINI_API_KEY is explicitly manipulated per-test via
monkeypatch rather than relying on whatever is in analysis/.env.
"""

from __future__ import annotations

import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
import requests

ANALYSIS_DIR = Path(__file__).resolve().parent.parent / "analysis"
if str(ANALYSIS_DIR) not in sys.path:
    sys.path.insert(0, str(ANALYSIS_DIR))

import llm.rca_second_opinion as rso


# ---------------------------------------------------------------------------
# call_gemini()
# ---------------------------------------------------------------------------

def _mock_response(text: str, prompt_tokens: int = 100, candidates_tokens: int = 20) -> MagicMock:
    resp = MagicMock()
    resp.status_code = 200
    resp.json.return_value = {
        "candidates": [{"content": {"parts": [{"text": text}]}}],
        "usageMetadata": {"promptTokenCount": prompt_tokens, "candidatesTokenCount": candidates_tokens},
    }
    resp.text = text
    return resp


def _mock_error_response(status_code: int, text: str = '{"error": {"message": "overloaded"}}') -> MagicMock:
    resp = MagicMock()
    resp.status_code = status_code
    resp.text = text
    return resp


def test_call_gemini_success(monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "fake-key")
    text = '{"decision": "confirm", "service": null, "confidence": "high", "reason": "matches"}'
    with patch.object(requests, "post", return_value=_mock_response(text, 111, 22)) as mock_post:
        result = rso.call_gemini("gemini-3.7-flash", "some prompt")

    mock_post.assert_called_once()
    assert result["decision"] == "confirm"
    assert result["confidence"] == "high"
    assert result["input_tokens"] == 111
    assert result["output_tokens"] == 22
    assert "error" not in result


def test_call_gemini_missing_key_does_not_call_network(monkeypatch):
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    with patch.object(requests, "post") as mock_post:
        result = rso.call_gemini("gemini-3.7-flash", "some prompt")

    mock_post.assert_not_called()
    assert "error" in result
    assert result["input_tokens"] == 0
    assert result["output_tokens"] == 0


def test_call_gemini_empty_key_does_not_call_network(monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "")
    with patch.object(requests, "post") as mock_post:
        result = rso.call_gemini("gemini-3.7-flash", "some prompt")

    mock_post.assert_not_called()
    assert "error" in result


def test_call_gemini_timeout(monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "fake-key")
    with patch.object(requests, "post", side_effect=requests.Timeout("timed out")):
        result = rso.call_gemini("gemini-3.7-flash", "some prompt")

    assert result == {"error": "gemini API timed out after 120s", "input_tokens": 0, "output_tokens": 0}


def test_call_gemini_network_exception_matches_other_callers_shape(monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "fake-key")
    with patch.object(requests, "post", side_effect=requests.ConnectionError("boom")):
        result = rso.call_gemini("gemini-3.7-flash", "some prompt")

    assert set(result) == {"error", "input_tokens", "output_tokens"}
    assert result["input_tokens"] == 0
    assert result["output_tokens"] == 0


def test_call_gemini_unparseable_answer(monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "fake-key")
    with patch.object(requests, "post", return_value=_mock_response("not json at all")):
        result = rso.call_gemini("gemini-3.7-flash", "some prompt")

    assert result["error"].startswith("unparseable:")


def test_call_gemini_retries_503_then_succeeds(monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "fake-key")
    text = '{"decision": "confirm", "service": null, "confidence": "high", "reason": "ok"}'
    responses = [_mock_error_response(503), _mock_error_response(503), _mock_response(text)]
    with patch.object(requests, "post", side_effect=responses) as mock_post, \
         patch.object(rso.time, "sleep") as mock_sleep:
        result = rso.call_gemini("gemini-3.7-flash", "some prompt")

    assert mock_post.call_count == 3
    assert mock_sleep.call_count == 2  # one sleep between each retry, none after success
    assert result["decision"] == "confirm"
    assert "error" not in result


def test_call_gemini_retries_429_then_succeeds(monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "fake-key")
    text = '{"decision": "propose", "service": "svc", "confidence": "low", "reason": "ok"}'
    responses = [_mock_error_response(429), _mock_response(text)]
    with patch.object(requests, "post", side_effect=responses), \
         patch.object(rso.time, "sleep"):
        result = rso.call_gemini("gemini-3.7-flash", "some prompt")

    assert result["decision"] == "propose"


def test_call_gemini_gives_up_after_max_retries(monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "fake-key")
    always_503 = _mock_error_response(503)
    with patch.object(requests, "post", return_value=always_503) as mock_post, \
         patch.object(rso.time, "sleep") as mock_sleep:
        result = rso.call_gemini("gemini-3.7-flash", "some prompt")

    assert mock_post.call_count == rso.GEMINI_MAX_RETRIES + 1
    assert mock_sleep.call_count == rso.GEMINI_MAX_RETRIES
    assert "error" in result
    assert "503" in result["error"]
    assert result["input_tokens"] == 0
    assert result["output_tokens"] == 0


def test_call_gemini_non_retryable_error_status_fails_immediately(monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "fake-key")
    bad_request = _mock_error_response(400, text='{"error": {"message": "bad request"}}')
    with patch.object(requests, "post", return_value=bad_request) as mock_post, \
         patch.object(rso.time, "sleep") as mock_sleep:
        result = rso.call_gemini("gemini-3.7-flash", "some prompt")

    mock_post.assert_called_once()
    mock_sleep.assert_not_called()
    assert "error" in result


# ---------------------------------------------------------------------------
# MODEL_REGISTRY caller dispatch
# ---------------------------------------------------------------------------

def test_ask_dispatches_claude_model_to_call_claude():
    case = {"case_id": "c1", "_bucket": "wrong_accepted", "algo_rank1": "svc-a"}
    original = dict(rso.MODEL_REGISTRY["claude-sonnet-5"])
    try:
        with patch.object(rso, "call_claude", return_value={"decision": "confirm", "input_tokens": 1, "output_tokens": 1}) as mc, \
             patch.object(rso, "call_codex") as mx, \
             patch.object(rso, "call_gemini") as mg:
            rso.MODEL_REGISTRY["claude-sonnet-5"]["caller"] = rso.call_claude
            rso.ask("claude-sonnet-5", case, "prompt")
        mc.assert_called_once()
        mx.assert_not_called()
        mg.assert_not_called()
    finally:
        rso.MODEL_REGISTRY["claude-sonnet-5"] = original


def test_ask_dispatches_codex_model_to_call_codex():
    case = {"case_id": "c1", "_bucket": "wrong_accepted", "algo_rank1": "svc-a"}
    original = dict(rso.MODEL_REGISTRY["gpt-5.6-luna"])
    try:
        with patch.object(rso, "call_claude") as mc, \
             patch.object(rso, "call_codex", return_value={"decision": "confirm", "input_tokens": 1, "output_tokens": 1}) as mx, \
             patch.object(rso, "call_gemini") as mg:
            rso.MODEL_REGISTRY["gpt-5.6-luna"]["caller"] = rso.call_codex
            rso.ask("gpt-5.6-luna", case, "prompt")
        mx.assert_called_once()
        mc.assert_not_called()
        mg.assert_not_called()
    finally:
        rso.MODEL_REGISTRY["gpt-5.6-luna"] = original


def test_ask_dispatches_gemini_model_to_call_gemini():
    case = {"case_id": "c1", "_bucket": "wrong_accepted", "algo_rank1": "svc-a"}
    original = dict(rso.MODEL_REGISTRY["gemini-3.7-flash"])
    try:
        with patch.object(rso, "call_claude") as mc, \
             patch.object(rso, "call_codex") as mx, \
             patch.object(rso, "call_gemini", return_value={"decision": "confirm", "input_tokens": 1, "output_tokens": 1}) as mg:
            rso.MODEL_REGISTRY["gemini-3.7-flash"]["caller"] = rso.call_gemini
            rso.ask("gemini-3.7-flash", case, "prompt")
        mg.assert_called_once()
        mc.assert_not_called()
        mx.assert_not_called()
    finally:
        rso.MODEL_REGISTRY["gemini-3.7-flash"] = original


def test_registry_dispatch_is_table_driven_not_if_chain():
    """Design-intent check: ask() must resolve the caller purely via
    MODEL_REGISTRY[model]["caller"] - swapping the registry entry for a model id
    changes which function ask() invokes, with zero branching logic in ask()
    itself. This is what lets a fourth vendor be added with just a new registry
    entry and a new call_<vendor>() function."""
    case = {"case_id": "c1", "_bucket": "wrong_accepted", "algo_rank1": "svc-a"}
    sentinel = MagicMock(return_value={"decision": "confirm", "input_tokens": 1, "output_tokens": 1})
    original = dict(rso.MODEL_REGISTRY["claude-sonnet-5"])
    try:
        rso.MODEL_REGISTRY["claude-sonnet-5"]["caller"] = sentinel
        rso.ask("claude-sonnet-5", case, "prompt")
    finally:
        rso.MODEL_REGISTRY["claude-sonnet-5"] = original
    sentinel.assert_called_once_with("claude-sonnet-5", "prompt")


# ---------------------------------------------------------------------------
# --models CLI argument (parse_models)
# ---------------------------------------------------------------------------

def test_parse_models_selects_exact_subset():
    result = rso.parse_models("gemini-3.7-flash,gemini-3.5-flash-lite")
    assert result == ["gemini-3.7-flash", "gemini-3.5-flash-lite"]
    assert "claude-sonnet-5" not in result
    assert "claude-haiku-4-5-20251001" not in result
    assert "gpt-5.6-luna" not in result
    assert "gpt-5.6-terra" not in result


def test_parse_models_default_is_every_registry_entry():
    result = rso.parse_models(",".join(rso.MODEL_REGISTRY))
    assert result == list(rso.MODEL_REGISTRY)


def test_parse_models_rejects_unknown_id():
    with pytest.raises(ValueError, match="unknown model id"):
        rso.parse_models("not-a-real-model")


def test_parse_models_strips_whitespace_and_drops_blanks():
    result = rso.parse_models(" claude-sonnet-5 , , gpt-5.6-luna ")
    assert result == ["claude-sonnet-5", "gpt-5.6-luna"]
