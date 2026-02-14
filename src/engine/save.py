import json
from pathlib import Path
from dataclasses import asdict
from src.tui.state import GameState


def save_game(state: GameState, filepath: Path) -> None:
    data = asdict(state)
    with open(filepath, "w") as f:
        json.dump(data, f, indent=4)


def load_game(filepath: Path) -> GameState:
    if not filepath.exists():
        raise FileNotFoundError(f"Save file not found: {filepath}")

    with open(filepath, "r") as f:
        data = json.load(f)

    return GameState(**data)
