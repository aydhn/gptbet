with open("sports_signal_bot/src/sports_signal_bot/inference/resolver.py", "r") as f:
    lines = f.readlines()

new_lines = []
skip = False
for line in lines:
    if "if model_res.fallback_reason ==" in line or "if getattr(model_res, 'fallback_reason'" in line:
        pass # don't add, clean up the duplicate lines I created
    elif "chain.warnings.append(\"Artifact is quarantined.\")" in line:
        pass
    else:
        new_lines.append(line)

with open("sports_signal_bot/src/sports_signal_bot/inference/resolver.py", "w") as f:
    f.writelines(new_lines)
