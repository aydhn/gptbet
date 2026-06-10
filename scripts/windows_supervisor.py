import subprocess
import time
import sys
import logging
import os

os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    filename="logs/windows_supervisor.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

MAX_RESTARTS = 3
COOLDOWN = 5

def run_bot():
    restarts = 0
    while restarts <= MAX_RESTARTS:
        logging.info(f"Starting bot (Attempt {restarts + 1}/{MAX_RESTARTS + 1})")
        print(f"[INFO] Starting bot (Attempt {restarts + 1}/{MAX_RESTARTS + 1})")

        env = os.environ.copy()
        env["PYTHONPATH"] = f"./src;{env.get('PYTHONPATH', '')}"

        # We start the CLI without args so it shows the help or runs default
        process = subprocess.Popen(
            [sys.executable, "-m", "sports_signal_bot.main", "--help"],
            env=env
        )

        try:
            process.wait()
            if process.returncode == 0:
                logging.info("Bot exited cleanly.")
                print("[INFO] Bot exited cleanly.")
                break
            else:
                logging.warning(f"Bot crashed with exit code {process.returncode}")
                print(f"[WARNING] Bot crashed with exit code {process.returncode}")
        except KeyboardInterrupt:
            logging.info("Supervisor interrupted. Terminating bot.")
            print("\n[INFO] Supervisor interrupted. Terminating bot.")
            process.terminate()
            break

        restarts += 1
        if restarts <= MAX_RESTARTS:
            logging.info(f"Waiting {COOLDOWN}s before restart...")
            time.sleep(COOLDOWN)

    if restarts > MAX_RESTARTS:
        logging.error("Max restarts reached. Supervisor terminating.")
        print("[ERROR] Max restarts reached. Supervisor terminating.")
        sys.exit(1)

if __name__ == "__main__":
    run_bot()
