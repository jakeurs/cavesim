from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Button, Header, Footer, Label
from textual.containers import Vertical, Center


class SettingsScreen(Screen):
    CSS = """
    SettingsScreen {
        align: center middle;
    }
    
    #settings_container {
        width: 50;
        height: auto;
        border: solid green;
    }
    
    Button {
        margin: 1;
        width: 100%;
    }
    """

    def compose(self) -> ComposeResult:
        yield Header()
        yield Center(
            Vertical(
                Label("Settings Placeholder"),
                Button("Back", id="back", variant="primary"),
                id="settings_container",
            )
        )
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "back":
            self.app.pop_screen()
