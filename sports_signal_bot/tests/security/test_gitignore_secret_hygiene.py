import os

def test_gitignore_contains_env_local():
    gitignore_path = os.path.join(os.path.dirname(__file__), "../../.gitignore")
    if os.path.exists(gitignore_path):
        with open(gitignore_path, "r") as f:
            content = f.read()
            assert ".env.local" in content
