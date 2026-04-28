with open("sports_signal_bot/src/sports_signal_bot/main.py", "r") as f:
    content = f.read()

import_str = "from sports_signal_bot.scheduler.cli import app as scheduler_app\napp.add_typer(scheduler_app, name=\"scheduler\", help=\"Scheduled orchestration engine\")"

if "from sports_signal_bot.release_management.cli import app as release_app" not in content:
    content = content.replace(import_str, import_str + "\n\nfrom sports_signal_bot.release_management.cli import app as release_app\napp.add_typer(release_app, name=\"release\", help=\"Release and promotion governance commands\")")

    with open("sports_signal_bot/src/sports_signal_bot/main.py", "w") as f:
        f.write(content)
