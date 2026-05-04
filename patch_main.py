import os
import re

def main():
    filepath = "src/sports_signal_bot/main.py"
    with open(filepath, "r") as f:
        content = f.read()

    # Add import
    import_stmt = "from sports_signal_bot.overlay_mesh_governance.cli import app as overlay_mesh_governance_app\n"
    if "overlay_mesh_governance_app" not in content:
        content = content.replace("import typer\n", "import typer\n" + import_stmt)

    # Add app.add_typer
    add_typer_stmt = "app.add_typer(overlay_mesh_governance_app, name=\"overlay-mesh-governance\", help=\"Overlay Mesh and Governance\")\n"
    if add_typer_stmt not in content:
        # Find the last app.add_typer and append
        lines = content.split('\n')
        for i in range(len(lines)-1, -1, -1):
            if "app.add_typer(" in lines[i]:
                lines.insert(i+1, add_typer_stmt)
                break
        content = '\n'.join(lines)

    with open(filepath, "w") as f:
        f.write(content)

if __name__ == "__main__":
    main()
