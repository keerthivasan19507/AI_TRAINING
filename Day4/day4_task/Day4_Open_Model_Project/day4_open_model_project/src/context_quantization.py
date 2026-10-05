"""Day 4 context-length and quantization experiment."""
from estimator import ModelConfig, estimate

BUDGET = 6.0
BASE_PARAMS = 4.02
ARCH = dict(layers=36, kv_heads=8, head_dim=128)

def run():
    print("DAY 4 CONTEXT / QUANTIZATION OBSERVATION")
    print(f"Memory budget: {BUDGET:.1f} GB")
    print("\nA. Change context, keep Q4 fixed")
    print(f"{'Context':>10} {'Weights GB':>12} {'KV GB':>10} {'Total GB':>11} {'Fits?':>7}")
    for ctx in [2048, 4096, 8192, 16384]:
        cfg = ModelConfig(f"Qwen3-4B Q4 {ctx}", BASE_PARAMS, "Q4", ctx, **ARCH)
        e = estimate(cfg, BUDGET)
        print(f"{ctx:>10} {e['weights_gb']:>12.2f} {e['kv_gb']:>10.2f} {e['total_gb']:>11.2f} {str(e['fits']):>7}")

    print("\nB. Change quantization, keep 8K context")
    print(f"{'Quant':>10} {'Weights GB':>12} {'KV GB':>10} {'Total GB':>11} {'Fits?':>7}")
    for q in ["Q2", "Q3", "Q4", "Q5", "Q6", "Q8"]:
        cfg = ModelConfig(f"Qwen3-4B {q}", BASE_PARAMS, q, 8192, **ARCH)
        e = estimate(cfg, BUDGET)
        print(f"{q:>10} {e['weights_gb']:>12.2f} {e['kv_gb']:>10.2f} {e['total_gb']:>11.2f} {str(e['fits']):>7}")

if __name__ == "__main__":
    run()
