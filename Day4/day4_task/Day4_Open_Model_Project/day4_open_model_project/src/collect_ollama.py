"""Capture the local Ollama state required by Day 4 section 3.4."""
from pathlib import Path
import subprocess
from datetime import datetime

OUT = Path(__file__).resolve().parents[1] / "screenshots" / "ollama_machine_output.txt"

def run_command(args):
    try:
        p = subprocess.run(args, capture_output=True, text=True, timeout=30)
        return p.returncode, p.stdout, p.stderr
    except FileNotFoundError:
        return 127, "", "Ollama was not found on PATH."
    except Exception as exc:
        return 1, "", str(exc)

def main():
    now = datetime.now().astimezone().isoformat()
    with OUT.open("w", encoding="utf-8") as f:
        f.write(f"Checked: {now}\n\n")
        for label, args in [("ollama list", ["ollama", "list"]), ("ollama ps", ["ollama", "ps"])]:
            code, stdout, stderr = run_command(args)
            f.write(f"=== {label} (exit code {code}) ===\n")
            f.write(stdout if stdout else stderr)
            f.write("\n\n")
    print(f"Saved: {OUT}")
    print("If Ollama is not installed, install/use it separately and rerun this script.")
if __name__ == "__main__":
    main()
