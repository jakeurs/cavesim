from dataclasses import dataclass, field
from typing import List


@dataclass
class GameState:
    shift_count: int = 0
    balance: float = 0.0
    debt: float = 1000.0
    current_location: str = "A"
    visited_locations: List[str] = field(default_factory=lambda: ["A"])


GLOBAL_STATE = GameState()
