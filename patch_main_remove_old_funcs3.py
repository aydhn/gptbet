with open("sports_signal_bot/src/sports_signal_bot/main.py", "r") as f:
    content = f.read()

import re
# Remove ingest-samples provider references
content = re.sub(r'provider: str = typer\.Option\("file_provider".*?,', '', content)
content = re.sub(r'config = _load_provider_config\(provider\)\n.*?f"\[bold green\]Starting ingestion for \{sport_enum\.value\} via \{provider\}\[/bold green\]"', 'console.print(f"[bold green]Starting ingestion for {sport_enum.value}[/bold green]")', content, flags=re.DOTALL)
content = re.sub(r'ingest_samples\(sport=sport, provider="file_provider"\)', 'ingest_samples(sport=sport)', content)
with open("sports_signal_bot/src/sports_signal_bot/main.py", "w") as f:
    f.write(content)
