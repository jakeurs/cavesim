from pathlib import Path
from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Button, Header, Footer
from textual.containers import Vertical, Center
from src.tui.state import GLOBAL_STATE
from src.engine.save import load_game

SAVE_FILE = Path("savegame.json")


class MainMenu(Screen):
    CSS = """
    MainMenu {
        align: center middle;
    }
    
    #menu_buttons {
        width: 40;
        height: auto;
    }
    
    Button {
        width: 100%;
        margin: 1 0;
    }
    """

    def compose(self) -> ComposeResult:
        yield Header()
        yield Center(
            Vertical(
                Button("New Shift", id="new_shift", variant="primary"),
                Button("Resume Shift", id="resume_shift"),
                Button("Settings", id="settings"),
                Button("Testing", id="testing_btn"),
                Button("Quit", id="quit", variant="error"),
                id="menu_buttons",
            )
        )
        yield Footer()

    def on_mount(self) -> None:
        if not SAVE_FILE.exists():
            self.query_one("#resume_shift", Button).disabled = True

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "quit":
            self.app.exit()
        elif event.button.id == "settings":
            self.app.push_screen("settings")
        elif event.button.id == "testing_btn":
            self.app.push_screen("testing")
        elif event.button.id == "new_shift":
            self.app.push_screen("map")
        elif event.button.id == "resume_shift":
            try:
                loaded_state = load_game(SAVE_FILE)
                GLOBAL_STATE.shift_count = loaded_state.shift_count
                GLOBAL_STATE.balance = loaded_state.balance
                GLOBAL_STATE.debt = loaded_state.debt
                GLOBAL_STATE.current_location = loaded_state.current_location
                GLOBAL_STATE.visited_locations = loaded_state.visited_locations
                self.app.push_screen("map")
                self.notify("Game Resumed")
            except Exception:
                self.notify("Failed to load save", severity="error")
