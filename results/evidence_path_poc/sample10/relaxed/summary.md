# Evidence path POC — sample10 / relaxed

| Measurement | Formula | Count | Result |
|---|---|---:|---:|
| Path Coverage (fault→symptom) | constructed / evaluated | 9 / 10 | 90.0% |
| RCA Path Coverage (rank1→symptom) | rca constructed / evaluated | 10 / 10 | 100.0% |
| Observed Edge Ratio | observed / returned edges | 29 / 30 | 96.7% |
| Supported Edge Ratio | supported / returned edges | 0 / 30 | 0.0% |
| Inferred Edge Ratio | inferred / returned edges | 1 / 30 | 3.3% |

## Rejection profile (fault seed)

| Reason | Count | Rate among rejected |
|---|---:|---:|
| required_horizontal_relationship_unavailable | 1 | 100.0% |

Evidence levels describe availability, not causal correctness.
