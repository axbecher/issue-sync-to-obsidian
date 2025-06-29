import subprocess
import sys

print("[RUNNER] Running tests before execution...")

result = subprocess.run(["python", "src/test.py"])
if result.returncode == 0:
    print("[RUNNER] ✅ Tests passed. Running main.py...\n")
    subprocess.run(["python", "src/main.py"])
else:
    print("[RUNNER] ❌ Tests failed. main.py will not run.")
    sys.exit(1)