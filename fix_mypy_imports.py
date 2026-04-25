import re

def fix_file(path, replacements):
    with open(path, "r") as f:
        content = f.read()
    for old, new in replacements:
        content = content.replace(old, new)
    with open(path, "w") as f:
        f.write(content)

fix_file("sports_signal_bot/src/sports_signal_bot/source_selection/scoring.py", [
    ("from typing import Dict, Tuple, List", "from typing import Dict, Tuple, List, Optional"),
    ("from typing import Dict, Optional, Tuple, List", "from typing import Dict, Optional, Tuple, List")
])

fix_file("sports_signal_bot/src/sports_signal_bot/source_selection/runner.py", [
    ("from typing import List, Dict, Any", "from typing import List, Dict, Any, Optional")
])
