import subprocess
import os

print("Running acceptance checks...")

def check(cmd, expect_text):
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, env={**os.environ, "PYTHONPATH": "src"})
    if expect_text in result.stdout or expect_text in result.stderr:
        print(f"OK: {cmd} passed ({expect_text} found)")
    else:
        print(f"FAIL: {cmd} missing '{expect_text}'\nOutput:\n{result.stdout}\n{result.stderr}")
        exit(1)

check("python -m sports_signal_bot.main final-validation-hardening preview-release-gating-report", "Mesh ID: test_mesh | Status: mesh_verified")
check("python -m sports_signal_bot.main final-validation-hardening preview-operator-proof-pack-report", "Pack ID: test_pack | Status: pack_verified")
check("python -m sports_signal_bot.main final-validation-hardening preview-replay-closure-report", "Compiler ID: test_compiler | Status: closure_verified")
check("python -m sports_signal_bot.main final-validation-hardening list-final-validation-strategies", "ConservativeFinalValidationStrategy")

print("All acceptance checks passed!")
