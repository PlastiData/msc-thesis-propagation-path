# Evidence path POC — sample_all / relaxed

| Measurement | Formula | Count | Result |
|---|---|---:|---:|
| Path Coverage (fault→symptom) | constructed / evaluated | 1262 / 1422 | 88.7% |
| RCA Path Coverage (rank1→symptom) | rca constructed / evaluated | 1179 / 1422 | 82.9% |
| Observed Edge Ratio | observed / returned edges | 4019 / 4242 | 94.7% |
| Supported Edge Ratio | supported / returned edges | 0 / 4242 | 0.0% |
| Inferred Edge Ratio | inferred / returned edges | 223 / 4242 | 5.3% |

## Rejection profile (fault seed)

| Reason | Count | Rate among rejected |
|---|---:|---:|
| no_connected_candidate_path | 64 | 40.0% |
| required_horizontal_relationship_unavailable | 95 | 59.4% |
| symptom_unavailable | 1 | 0.6% |

Evidence levels describe availability, not causal correctness.
