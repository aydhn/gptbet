with open("sports_signal_bot/src/sports_signal_bot/inference/resolver.py", "r") as f:
    content = f.read()

content = content.replace("chain.model_artifact_id = model_res.resolved_id", "chain.model_artifact_id = model_res.resolved_id\n            if getattr(model_res, 'fallback_reason', None) == \"Artifact is quarantined.\":\n                chain.warnings.append(\"Artifact is quarantined.\")")

with open("sports_signal_bot/src/sports_signal_bot/inference/resolver.py", "w") as f:
    f.write(content)
