# Evidence labels

| Label | Meaning on this pack |
|---|---|
| Observed | Structural and statistical checks pass; hop is directly backed by telemetry |
| Supported | Weaker mix of checks; still labelled, not dropped |
| Inferred | Assumed hop; names what is missing (e.g. no usable temporal order) |
| insufficient_evidence | No path returned; refusal is a result and stays in every denominator |

Supported edges rarely fire on this pack; temporal order is often unknown. That reflects dataset limits, not a hidden accuracy score.
