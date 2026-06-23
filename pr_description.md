🔒 Use safe_load instead of load for yaml

🎯 **What:**
Replaced `yaml.load` (with fallback to `yaml.safe_load`) with `yaml.safe_load` exclusively in `src/sports_signal_bot/ecosystem_sync/cli.py`.

⚠️ **Risk:**
Using `yaml.load`, even when conditionally trying to apply `CSafeLoader`, is inherently risky. If `CSafeLoader` is missing, or the logic surrounding the check breaks, `yaml.load` can be invoked with standard loaders, permitting execution of arbitrary Python functions/objects contained within a malicious YAML file. This can lead to Remote Code Execution (RCE) and full compromise of the environment if an attacker manages to supply malicious configuration files.

🛡️ **Solution:**
The function `load_config` was updated to explicitly and exclusively call `yaml.safe_load(f)`. This guarantees that only a safe subset of standard YAML tags can be resolved, completely preventing the instantiation of arbitrary Python objects, while still parsing legitimate configurations flawlessly.
