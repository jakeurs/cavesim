from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Button, Header, Footer, Label
from textual.containers import Vertical, Center


class TestingScreen(Screen):
    CSS = """
    TestingScreen {
        align: center middle;
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
                Label("Testing Dashboard"),
                Button("Run Unit Tests", id="test_unit"),
                Button("Run Integration Tests", id="test_integration"),
                Button("Back to Menu", id="back_btn", variant="error"),
            )
        )
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "back_btn":
            self.app.pop_screen()
        elif event.button.id == "test_unit":
            self.notify("Running Unit Tests (Mocked)")
        elif event.button.id == "test_integration":
            self.notify("Running Integration Tests (Mocked)")
