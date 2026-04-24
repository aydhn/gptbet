import yaml
from pathlib import Path
from sports_signal_bot.core.constants import SportType
from sports_signal_bot.data.normalization.names import normalize_team_name
import logging

logger = logging.getLogger(__name__)

class TeamResolver:
    def __init__(self, aliases_path: Path):
        self.aliases_path = aliases_path
        self._aliases = {}
        self._load_aliases()

    def _load_aliases(self):
        if not self.aliases_path.exists():
            logger.warning(f"Aliases file not found at {self.aliases_path}. Resolution will fallback to normalization.")
            return

        with open(self.aliases_path, 'r') as f:
            raw_aliases = yaml.safe_load(f)

        if not raw_aliases:
            return

        for sport, leagues in raw_aliases.items():
            if sport not in self._aliases:
                self._aliases[sport] = {}
            for league, teams in leagues.items():
                if league not in self._aliases[sport]:
                    self._aliases[sport][league] = {}
                for canonical_name, aliases in teams.items():
                    for alias in aliases:
                        normalized_alias = normalize_team_name(alias).lower()
                        self._aliases[sport][league][normalized_alias] = canonical_name

    def resolve_team_name(self, name: str, sport: str, league: str) -> str:
        """Resolves a team name to its canonical name using aliases, or falls back to basic normalization."""
        normalized_input = normalize_team_name(name)
        lower_input = normalized_input.lower()

        if sport in self._aliases and league in self._aliases[sport]:
            if lower_input in self._aliases[sport][league]:
                return self._aliases[sport][league][lower_input]

        # Fallback
        logger.debug(f"Unresolved alias for '{name}' in {sport}/{league}. Using normalized fallback.")
        return normalized_input
