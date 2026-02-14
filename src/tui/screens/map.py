from pathlib import Path
from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Button, Label, Header, Footer
from textual.containers import Grid, Container
from src.tui.state import GLOBAL_STATE
from src.engine.save import save_game, load_game

SAVE_FILE = Path("savegame.json")


class MapScreen(Screen):
    CSS = """
    MapScreen {
        align: center middle;
    }
    #map-grid {
        layout: grid;
        grid-size: 3 3;
        grid-gutter: 1 2;
        padding: 2;
    }
    Button {
        width: 100%;
    }
    """

    def compose(self) -> ComposeResult:
        yield Header()
        yield Container(
            Label(
                f"Current Location: {GLOBAL_STATE.current_location}",
                id="location-label",
            ),
            Grid(
                Button("A", id="node-A"),
                Button("B", id="node-B"),
                Button("C", id="node-C"),
                Button("D", id="node-D"),
                Button("E", id="node-E"),
                Button("F", id="node-F"),
                id="map-grid",
            ),
            Button("Save Game", id="save-btn", variant="success"),
            Button("Load Game", id="load-btn", variant="warning"),
            Button("Back to Menu", id="back-btn"),
            id="map-container",
        )
        yield Footer()

    def on_mount(self) -> None:
        self.update_location_label()

    def update_location_label(self) -> None:
        self.query_one("#location-label", Label).update(
            f"Current Location: {GLOBAL_STATE.current_location}"
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        btn_id = event.button.id
        if btn_id == "back-btn":
            self.app.pop_screen()
        elif btn_id == "save-btn":
            save_game(GLOBAL_STATE, SAVE_FILE)
            self.notify("Game Saved!")
        elif btn_id == "load-btn":
            try:
                loaded_state = load_game(SAVE_FILE)
                GLOBAL_STATE.shift_count = loaded_state.shift_count
                GLOBAL_STATE.balance = loaded_state.balance
                GLOBAL_STATE.debt = loaded_state.debt
                GLOBAL_STATE.current_location = loaded_state.current_location
                GLOBAL_STATE.visited_locations = loaded_state.visited_locations
                self.update_location_label()
                self.notify("Game Loaded!")
            except FileNotFoundError:
                self.notify("No save file found.", severity="error")
        elif btn_id and btn_id.startswith("node-"):
            node = btn_id.split("-")[1]
            GLOBAL_STATE.current_location = node
            if node not in GLOBAL_STATE.visited_locations:
                GLOBAL_STATE.visited_locations.append(node)
            self.update_location_label()
            self.app.push_screen("shift")
