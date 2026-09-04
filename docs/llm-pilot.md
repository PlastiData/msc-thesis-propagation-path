# LLM second opinion (pilot)

Separate from path construction. Models see the algorithm seed plus redacted evidence; they never see the injection label in the prompt.

- **4080 rows** in pilot_results.json (680 cases × 6 models), 0 errors.
- Models: claude-haiku-4-5-20251001, claude-sonnet-5, gemini-3.5-flash-lite, gemini-3.7-flash, gpt-5.6-luna, gpt-5.6-terra.
- Answers: confirm / propose / insufficient.
- **Tokens (pilot totals):** input 69,453,064, output 1,954,138. List-price sum in JSON: $103.68 (Claude/Codex billed as subscription in the runner; Gemini is metered API — see row-level fields, do not treat as thesis accuracy).

- claude-haiku-4-5-20251001: 680 rows
- claude-sonnet-5: 680 rows
- gemini-3.5-flash-lite: 680 rows
- gemini-3.7-flash: 680 rows
- gpt-5.6-luna: 680 rows
- gpt-5.6-terra: 680 rows

This pilot does not change the accept policy behind path coverage.
