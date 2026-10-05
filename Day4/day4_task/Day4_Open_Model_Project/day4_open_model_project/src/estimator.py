"""Day 4 memory estimator.

Formula:
weights = parameters(B) * bytes_per_parameter
KV cache = 2 * layers * KV_heads * head_dim * context_tokens * KV_bytes
total = weights + KV cache + runtime overhead

The KV formula assumes K and V are both stored and uses the KV precision supplied
by the user. The overhead percentage is an intentionally conservative estimate.
This is a fit estimator, not a prediction of exact process memory.
"""
from dataclasses import dataclass

BYTES_PER_PARAM = {
    "FP32": 4.0,
    "FP16": 2.0,
    "BF16": 2.0,
    "Q8": 1.0,
    "Q6": 0.75,
    "Q5": 0.625,
    "Q4": 0.5,
    "Q3": 0.375,
    "Q2": 0.25,
}

@dataclass
class ModelConfig:
    name: str
    params_b: float
    precision: str
    context: int
    layers: int
    kv_heads: int
    head_dim: int
    kv_bytes: float = 2.0  # FP16 KV cache
    overhead_fraction: float = 0.10

def estimate(cfg: ModelConfig, memory_budget_gb: float):
    weights_gb = cfg.params_b * BYTES_PER_PARAM[cfg.precision]
    kv_bytes = 2 * cfg.layers * cfg.kv_heads * cfg.head_dim * cfg.context * cfg.kv_bytes
    kv_gb = kv_bytes / 1_000_000_000
    overhead_gb = (weights_gb + kv_gb) * cfg.overhead_fraction
    total_gb = weights_gb + kv_gb + overhead_gb
    return {
        "weights_gb": weights_gb,
        "kv_gb": kv_gb,
        "overhead_gb": overhead_gb,
        "total_gb": total_gb,
        "fits": total_gb <= memory_budget_gb,
    }

def print_row(cfg, budget):
    e = estimate(cfg, budget)
    print(
        f"{cfg.name:30} {cfg.params_b:5.2f}B {cfg.precision:>5} "
        f"{cfg.context:>6} {e['weights_gb']:>7.2f} {e['kv_gb']:>7.2f} "
        f"{e['total_gb']:>7.2f} {'YES' if e['fits'] else 'NO'}"
    )

def main():
    budget = 6.0
    # Qwen3-4B architecture values are from the official Qwen config:
    # 36 layers, 8 KV heads, head_dim 128.
    configs = [
        ModelConfig("Qwen3-4B Q4, 4K", 4.02, "Q4", 4096, 36, 8, 128),
        ModelConfig("Qwen3-4B Q4, 8K", 4.02, "Q4", 8192, 36, 8, 128),
        ModelConfig("Qwen3-4B Q4, 16K", 4.02, "Q4", 16384, 36, 8, 128),
        ModelConfig("Qwen3-4B Q8, 8K", 4.02, "Q8", 8192, 36, 8, 128),
    ]
    print("DAY 4 MEMORY ESTIMATOR")
    print(f"Available memory budget: {budget:.1f} GB")
    print("Assumed KV precision: FP16 (2 bytes/value); runtime overhead: 10%")
    print("-" * 105)
    print(f"{'Model':30} {'Params':>7} {'Prec':>5} {'Ctx':>6} {'Weights':>7} {'KV':>7} {'Total':>7} {'Fits':>4}")
    print("-" * 105)
    for cfg in configs:
        print_row(cfg, budget)

if __name__ == "__main__":
    main()
