# Evidence path POC — sample_all / strict

| Measurement | Formula | Count | Result |
|---|---|---:|---:|
| Path Coverage (fault→symptom) | constructed / evaluated | 1048 / 1422 | 73.7% |
| RCA Path Coverage (rank1→symptom) | rca constructed / evaluated | 1027 / 1422 | 72.2% |
| Observed Edge Ratio | observed / returned edges | 3454 / 3454 | 100.0% |
| Supported Edge Ratio | supported / returned edges | 0 / 3454 | 0.0% |
| Inferred Edge Ratio | inferred / returned edges | 0 / 3454 | 0.0% |

## Rejection profile (fault seed)

| Reason | Count | Rate among rejected |
|---|---:|---:|
| no_connected_candidate_path | 64 | 17.1% |
| required_horizontal_relationship_unavailable | 309 | 82.6% |
| symptom_unavailable | 1 | 0.3% |

Evidence levels describe availability, not causal correctness.
