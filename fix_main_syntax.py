import re

with open("src/sports_signal_bot/main.py", "r") as f:
    lines = f.readlines()

new_lines = []
for line in lines:
    if line.strip() == 'app.add_typer(overlay_mesh_governance_app, name="overlay-mesh-governance", help="Overlay Mesh and Governance")':
        continue
    new_lines.append(line)

# find the right place to add it (e.g. around line 110 where other app.add_typer are)
insert_idx = -1
for i, line in enumerate(new_lines):
    if line.startswith('app.add_typer(corridor_governance_app'):
        insert_idx = i + 1

if insert_idx != -1:
    new_lines.insert(insert_idx, 'app.add_typer(overlay_mesh_governance_app, name="overlay-mesh-governance", help="Overlay Mesh and Governance")\n')

with open("src/sports_signal_bot/main.py", "w") as f:
    f.writelines(new_lines)
