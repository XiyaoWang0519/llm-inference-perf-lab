# LLM Inference Perf Lab

Small lab for measuring LLM inference latency on a local or Colab GPU using an OpenAI-compatible vLLM endpoint.

## Layout

```text
llm-inference-perf-lab/
├── notebooks/
│   ├── client_colab.ipynb   # Colab: serve + client + latency sweeps
│   └── vllm_setup.ipynb     # Colab vLLM install / serve helper
├── src/
│   └── client.py            # Minimal OpenAI-compatible client
├── results/
│   └── run_YYYY-MM-DD/      # Dated benchmark artifacts
├── requirements.txt
└── .gitignore
```

## Quick start (Colab)

1. Open `notebooks/client_colab.ipynb` in Google Colab with a GPU runtime.
2. Run cells top to bottom: install → start vLLM → wait until ready → client requests.
3. Section 10 writes a latency sweep CSV with per-request token usage.

Local helper client:

```bash
pip install -r requirements.txt
python src/client.py
```

Point `BASE_URL` / `MODEL_NAME` in `src/client.py` at your OpenAI-compatible server.

## Metrics notes

- `output_tokens_per_s` / `output_tokens_per_e2e_s` means `completion_tokens / end_to_end_latency`.
  That rate includes prefill, scheduling, and HTTP overhead; it is not pure decode throughput.
- Prefer recording actual `response.usage` token counts on every request; do not assume
  `completion_tokens == max_tokens`.
