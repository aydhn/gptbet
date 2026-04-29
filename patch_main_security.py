import sys

with open('sports_signal_bot/src/sports_signal_bot/main.py', 'r') as f:
    content = f.read()

# Add security cli
if 'from sports_signal_bot.main_security_cli import app as security_app' not in content:
    content = content.replace(
        'if __name__ == "__main__":',
        'from sports_signal_bot.main_security_cli import app as security_app\napp.add_typer(security_app, name="security", help="Security and Config Governance Commands")\n\nif __name__ == "__main__":'
    )

with open('sports_signal_bot/src/sports_signal_bot/main.py', 'w') as f:
    f.write(content)
