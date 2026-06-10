import sys
import os

def check_python_version():
    if sys.version_info < (3, 12):
        print("[ERROR] Python 3.12+ is required.")
        return False
    return True

def check_dependencies():
    try:
        import typer
        import pydantic
        import yaml
        return True
    except ImportError as e:
        print(f"[ERROR] Missing dependency: {e}")
        return False

def check_env():
    if not os.path.exists(".env"):
        print("[WARNING] .env file not found. Proceeding with defaults.")
    return True

def check_log_path():
    os.makedirs("logs", exist_ok=True)
    try:
        with open("logs/healthcheck_test.log", "w") as f:
            f.write("test")
        os.remove("logs/healthcheck_test.log")
        return True
    except IOError:
        print("[ERROR] Cannot write to logs/ directory.")
        return False

if __name__ == "__main__":
    print("[INFO] Running healthcheck...")
    if all([check_python_version(), check_dependencies(), check_env(), check_log_path()]):
        print("[INFO] Healthcheck passed.")
        sys.exit(0)
    else:
        print("[ERROR] Healthcheck failed.")
        sys.exit(1)
