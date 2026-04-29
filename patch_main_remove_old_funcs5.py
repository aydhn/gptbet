with open("sports_signal_bot/src/sports_signal_bot/main.py", "r") as f:
    content = f.read()

import re
content = re.sub(r'    console\.print\(f"\[bold green\]Starting ingestion for \{sport_enum\.value\}\[/bold green\]"\)\n    \)\n\n    fixture_manifest = orchestrator\.ingest_fixtures\(fixture_prov, sport_enum\)', '    console.print(f"[bold green]Starting ingestion for {sport_enum.value}[/bold green]")\n\n    fixture_manifest = orchestrator.ingest_fixtures(None, sport_enum)', content)

content = re.sub(r'odds_manifest = orchestrator\.ingest_odds\(odds_prov, sport_enum\)', 'odds_manifest = orchestrator.ingest_odds(None, sport_enum)', content)
content = re.sub(r'stats_manifest = orchestrator\.ingest_stats\(stats_prov, sport_enum\)', 'stats_manifest = orchestrator.ingest_stats(None, sport_enum)', content)

with open("sports_signal_bot/src/sports_signal_bot/main.py", "w") as f:
    f.write(content)
