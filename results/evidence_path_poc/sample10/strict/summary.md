# Evidence path POC — sample10 / strict

| Measurement | Formula | Count | Result |
|---|---|---:|---:|
| Path Coverage (fault→symptom) | constructed / evaluated | 8 / 10 | 80.0% |
| RCA Path Coverage (rank1→symptom) | rca constructed / evaluated | 9 / 10 | 90.0% |
| Observed Edge Ratio | observed / returned edges | 27 / 27 | 100.0% |
| Supported Edge Ratio | supported / returned edges | 0 / 27 | 0.0% |
| Inferred Edge Ratio | inferred / returned edges | 0 / 27 | 0.0% |

## Rejection profile (fault seed)

| Reason | Count | Rate among rejected |
|---|---:|---:|
| required_horizontal_relationship_unavailable | 2 | 100.0% |

Evidence levels describe availability, not causal correctness.
