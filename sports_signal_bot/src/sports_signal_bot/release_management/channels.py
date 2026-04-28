from enum import Enum

class ReleaseChannel(str, Enum):
    draft = "draft"
    candidate = "candidate"
    canary = "canary"
    stable = "stable"
    frozen = "frozen"
    quarantined = "quarantined"
    rolled_back = "rolled_back"
    archived = "archived"
