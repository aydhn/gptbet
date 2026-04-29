from typing import List
import typer

class CommandSafetyGate:
    def __init__(self, risky_commands: List[str] = None, confirmation_required: List[str] = None):
        self.risky_commands = risky_commands or ["run-dispatch", "run-release"]
        self.confirmation_required = confirmation_required or ["run-dispatch"]

    def check_command_safety(self, command_name: str, mode: str = "production", confirm: bool = False):
        if mode == "dry_run_preview":
            return True # Dry run implies safety

        if command_name in self.risky_commands:
            if command_name in self.confirmation_required and not confirm:
                typer.echo(f"Security Gate Blocked: Command {command_name} requires explicit confirmation (--confirm).", err=True)
                return False

        return True
