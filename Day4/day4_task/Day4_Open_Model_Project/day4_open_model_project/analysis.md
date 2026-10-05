## 3.4 Estimate versus reality

The Day 4 task requires checking at least one model that is actually installed locally using `ollama list` and `ollama ps`. My laptop has **Qwen2.5:1.5b** installed and running through Ollama.

The `ollama list` result showed:

| Model        | ID           |   Size |
| ------------ | ------------ | -----: |
| qwen2.5:1.5b | 65ec06548149 | 986 MB |

The `ollama ps` result from the running model showed:

| Model        | ID           | Runtime size | Processor | Context |
| ------------ | ------------ | -----------: | --------- | ------: |
| qwen2.5:1.5b | 65ec06548149 |       1.2 GB | 100% CPU  |    4096 |

The runtime therefore used the CPU rather than a GPU or a CPU/GPU split. The 1.2 GB runtime size is higher than the 986 MB size reported by `ollama list`. This difference is expected because the model file size and the memory used by a running process are not necessarily the same. Runtime memory can include the loaded model, KV cache, buffers and other backend/runtime allocations.

This runtime check is not a direct same-model comparison with the Qwen3-4B estimator experiment. The estimator experiment uses Qwen3-4B, while the model actually installed on this laptop is Qwen2.5:1.5b. Therefore, I use the Ollama result as a real-machine validation of the general memory-estimation idea rather than claiming that the 1.2 GB runtime value is the measured value of the Qwen3-4B 3.54 GB estimate.

For the main Qwen3-4B scenario, the 8K Q4 estimate is **2.01 GB of weights + 1.21 GB of KV cache = 3.22 GB before the 10% overhead allowance, or 3.54 GB including that allowance**. The actual Ollama process can differ from a simplified estimate because of the exact quantized build, runtime allocations, context settings, backend implementation and other memory overheads.

The screenshots `ollama_list.png` and `ollama_ps.png` provide the machine-specific evidence for this section.

