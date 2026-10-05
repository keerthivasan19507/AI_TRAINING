# Day 4 — Will It Fit, and May I Use It?

This project implements the Day 4 task from `Day4_Task.docx.pdf`.

## Scenario
- Machine: 8 GB RAM laptop, CPU-only local serving
- Practical memory budget used for the exercise: 6 GB
- Purpose: private college coding/summarisation helper
- User: one student
- Models compared: Qwen3-4B, Gemma 3 4B, Llama 3.2 3B

The estimator is intentionally an estimate. It uses parameter count, bytes/parameter, KV-cache size and a runtime-overhead allowance. Real Ollama usage can differ because of architecture, build, context defaults, backend and other runtime allocations.

## Run
```powershell
python src/estimator.py
python src/context_quantization.py
python src/collect_ollama.py
```

`collect_ollama.py` records `ollama list` and `ollama ps` when Ollama is installed.

## Repository layout
- `analysis.md` — complete written analysis
- `src/estimator.py` — memory estimator
- `src/context_quantization.py` — context and quantization experiment
- `src/collect_ollama.py` — captures local Ollama reality
- `screenshots/` — text outputs from the estimator experiments; replace/add screenshots from the local terminal
