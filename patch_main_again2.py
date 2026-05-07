with open("src/sports_signal_bot/main.py", "r") as f:
    content = f.read()

content = content.replace('if __name__ == "__main__":\n    app()\n\nfrom sports_signal_bot.cli_global_hardening import app as global_hardening_app\napp.add_typer(global_hardening_app, name="global-hardening", help="Post-100 Hardening Pack 11: Global Hardening")\n', 'from sports_signal_bot.cli_global_hardening import app as global_hardening_app\napp.add_typer(global_hardening_app, name="global-hardening", help="Post-100 Hardening Pack 11: Global Hardening")\n\nif __name__ == "__main__":\n    app()\n')

with open("src/sports_signal_bot/main.py", "w") as f:
    f.write(content)
