# vLLM Notes

## Environment

- GPU: NVIDIA Tesla T4, 15360 MiB
- CUDA driver: 13.0
- PyTorch: 2.9.0+cu128
- vLLM: 0.11.2
- Model: Qwen/Qwen2.5-1.5B-Instruct
- Serving interface: OpenAI-compatible Chat Completions API
- Prompt tokens: 36
- Maximum generated tokens: 100
- Temperature: 0.0

## Completed Experiments

### Single Request

The client sends a request to the OpenAI-compatible vLLM endpoint and
measures end-to-end latency using `time.perf_counter()`.

The reported output-token rate includes HTTP overhead, request scheduling,
prefill, and decoding. It is therefore an end-to-end application metric,
not pure decode throughput.

### Streaming Request

The streaming experiment measures:

- Time to first token
- End-to-end request time
- Generated output

### Concurrency Sweep

Tested concurrency levels:

- 1
- 2
- 4
- 8

Each concurrency level was repeated three times. Every request used the
same prompt and generated 100 output tokens.

Results:

| Concurrency | Mean latency (s) | Aggregate output tokens/s | Scaling efficiency |
|---:|---:|---:|---:|
| 1 | 1.649 | 60.63 | 100.0% |
| 2 | 1.669 | 119.13 | 98.2% |
| 4 | 1.711 | 232.21 | 95.8% |
| 8 | 1.767 | 449.82 | 92.7% |

Mean request latency increased by approximately 7.1% between concurrency
1 and concurrency 8, while aggregate output throughput improved by
approximately 7.42x.

For this workload, vLLM increased total server throughput with only a
modest request-latency penalty.

## Questions and Observations

1. How does vLLM dynamically batch requests that arrive close together?
2. At what concurrency level will request queuing cause latency to rise sharply?
3. How should prefill throughput and decode throughput be measured separately?
4. The first request after server startup was substantially slower, suggesting
   that benchmark runs should include a warm-up stage.
5. End-to-end output tokens per second should not be presented as pure model
   decode throughput.

## Current Limitations

The current conclusions apply only to:

- NVIDIA Tesla T4
- Qwen2.5-1.5B-Instruct
- Short 36-token prompts
- 100 generated tokens per request
- Concurrency levels up to 8

The results do not yet demonstrate performance under long prompts, higher
concurrency, or different output lengths.
