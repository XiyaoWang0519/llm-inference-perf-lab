# Initial T4 latency benchmark — 2026-07-12

Source: `notebooks/client_colab.ipynb`  
Raw rows: `latency_raw.csv`  
Machine-readable: `run.json`

This run is a first successful T4 smoke test: it validates the harness, result
schema, and basic latency measurement. It is not intended for strong performance
claims.

## Environment

| Item | Value |
|---|---|
| GPU | Tesla T4 (15360 MiB) |
| CUDA | 13.0 (driver 580.82.07) |
| PyTorch | 2.9.0+cu128 |
| vLLM | 0.11.2 |
| Model | Qwen/Qwen2.5-1.5B-Instruct (`qwen2.5-1.5b`) |
| Prompt | What is LLM inference latency? |
| Prompt tokens | 36 (from single-request `usage`) |
| max_tokens / temperature | 100 / 0.0 |
| Warmup / measured | 1 / 5 |

## Single request

| Metric | Value |
|---|---|
| latency_s | 4.887 |
| prompt_tokens | 36 |
| completion_tokens | 100 |
| total_tokens | 136 |
| output_tokens_per_e2e_s | 20.46 |

`output_tokens_per_e2e_s` is `completion_tokens / end_to_end_latency`. It includes prefill, scheduling, and HTTP overhead, and is not pure decode throughput.

## Streaming request

| Metric | Value |
|---|---|
| ttft_s | 0.079 |
| e2e_latency_s | 2.082 |
| output_chars | 548 |

This run did not record stream `usage` / `completion_tokens`. Streaming and non-streaming latencies are therefore not directly comparable.

## Latency sweep

| run | is_warmup | latency_s | prompt_tokens | completion_tokens | total_tokens | output_tokens_per_s |
|---|---|---|---|---|---|---|
| 1 | true | 2.066 | | | | |
| 1 | false | 2.200 | | | | |
| 2 | false | 2.460 | | | | |
| 3 | false | 2.565 | | | | |
| 4 | false | 2.702 | | | | |
| 5 | false | 2.679 | | | | |

| summary (measured runs only) | value |
|---|---|
| n | 5 |
| mean_s | 2.521 |
| sample_stdev_s | 0.204 |
| min_s | 2.200 |
| max_s | 2.702 |
| CV | ~8.1% |

Standard deviation is the sample standard deviation (`statistics.stdev`, `ddof=1`) across the five measured runs.

**Token columns:** This Colab run’s sweep cell only logged latency. Per-run `response.usage` was not captured, so token columns are blank on purpose — do not copy `completion_tokens=100` from the single-request row or assume `max_tokens`. The notebook now records usage on every sweep row for future runs.

## Initial observations

- The first standalone non-streaming request took 4.887 seconds, substantially longer than the later sweep requests. This may reflect first-run, runtime-state, or other transient overhead, but the cause was not isolated in this experiment.
- After one explicit warmup request, five measured requests had a mean end-to-end latency of 2.521 seconds with a standard deviation of 0.204 seconds.
- Measured latencies trended upward across early runs (`2.200 → 2.460 → 2.565 → 2.702 → 2.679`); cause is not established.
- The streaming request produced the first token after 79 ms and completed after 2.082 seconds.
- Streaming and non-streaming results are not yet directly comparable because token usage was not recorded for the streaming request.
- Future runs should record prompt and completion token counts for every request.
