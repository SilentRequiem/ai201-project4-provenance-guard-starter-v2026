# Unit 9 AFTER capstone evaluation

Created by capstone_eval.py using real local HTTP responses and JSONL logs.

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Logging completeness and 1 MiB rotation | 10/10 detailed records and safe 1 MiB rotation | 10/10 with rotation=True | 10/10 with rotation=True | 10/10 with rotation=True | **MET** |
| 2. Timing accuracy | 10/10 client vs server gaps <= 200 ms | 10/10 gaps <= 200 ms | 10/10 gaps <= 200 ms | 10/10 gaps <= 200 ms | **MET** |
| 3. Log persistence | 10/10 service logs survive restart including archived history | 10/10 after restart; archived probe=True | 10/10 after restart; archived probe=True | 10/10 after restart; archived probe=True | **MET** |
| 4. Failure logging | 5/5 invalid requests have their own detailed logs | 5/5 valid rejection traces | 5/5 valid rejection traces | 5/5 valid rejection traces | **MET** |
| 5. Average warm response time | Mean of ten warm requests < 2 seconds | 0.122 seconds | 0.154 seconds | 0.116 seconds | **MET** |

## Measured cost

Measured successful warm requests: 30
Mean client seconds: 0.130634
Mean server seconds: 0.113908
Mean process CPU seconds: 0.960938
100 sequential requests/day: 13.063 client-wait seconds and 96.094 process CPU seconds at the measured mean.

Complete HTTP responses, timing values, archived-log fixture results, and per-criterion traces are in the JSON file.
This is measured local compute time, not API spend or a hosting bill.
No after-run success is claimed until the actual AFTER script runs.
