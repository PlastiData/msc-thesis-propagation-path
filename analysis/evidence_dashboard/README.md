# Evidence dashboard (how to view it)

The dashboard is **generated static HTML** next to the POC outputs — same idea as
`litreview-webapp` pages (structured sections + tables), without a second npm app.

## View (talk root = strict)

```bash
cd rcabench-platform-feat-fse26
.venv/bin/python analysis/cli.py --sample analysis/samples/sample10.txt --policy strict
.venv/bin/python analysis/cli.py --sample analysis/samples/sample10.txt --policy relaxed

cd results/evidence_path_poc/sample10/strict
python3 -m http.server 8765
# open http://127.0.0.1:8765/
```

Prefer **strict** as the presentation root. Regenerate both policies so the RQ-A
sibling strip can load `../relaxed/summary.json`.

## What the index shows (top → bottom)

1. Claim — candidate path under an evidence policy (not causal GT)
2. Filter — all / differ / refuse / same
3. **Investigation queue** — agree tag, inject/RCA verdicts + path strips, link to case
4. **Evaluation metrics** — collapsed `<details>`: RQ-A (+ sibling), RQ-C, agreement, RQ-B, AC@k footnote

Case pages: verdict banner (ACCEPT/REFUSE, injection window) → dual-path strips →
hop evidence (route, calls/errors, trace ids, stat numbers; no Why / per-hop Time) →
timeline anchors (not a full Gantt) → rankings secondary.

## Archive (previous RQ-first UI)

Frozen copy of the pre-console layout (RQ tables first):

`results/evidence_path_poc/_snapshot_rq_first_20260804/`

Open `…/_snapshot_rq_first_20260804/sample10/strict/index.html`. Live regen never writes into `_snapshot_*`.

Industry UX refs (what was stolen for this console): `../docs/INDUSTRY_UX.md`.

## Why not a new npm webapp yet

`litreview-webapp` is a full Express + SPA pipeline UI. For this POC the data is
already rendered into `index.html` / `graph.html` at generation time. A second
Node stack would duplicate that without changing the measurements. If a live
filterable SPA becomes necessary later, start from the litreview pattern and
read `summary.json` — do not fork a heavy frontend before the science is stable.
