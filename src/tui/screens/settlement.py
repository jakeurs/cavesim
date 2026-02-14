from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Button, Label, Header, Footer
from textual.containers import Vertical, Center
from src.tui.state import GLOBAL_STATE


class SettlementScreen(Screen):
    CSS = """
    SettlementScreen {
        align: center middle;
    }
    """

    def compose(self) -> ComposeResult:
        yield Header()
        yield Center(
            Vertical(
                Label(f"Current Debt: ${GLOBAL_STATE.debt}", id="debt-label"),
                Button("Pay $100", id="pay-100"),
                Button("Next Assignment", id="next_assignment"),
                Button("Back to Menu", id="back-btn"),
            )
        )
        yield Footer()

    def on_mount(self) -> None:
        self.update_debt_label()

    def update_debt_label(self) -> None:
        self.query_one("#debt-label", Label).update(
            f"Current Debt: ${GLOBAL_STATE.debt}"
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        btn_id = event.button.id
        if btn_id == "back-btn":
            self.app.pop_screen()
        elif btn_id == "pay-100":
            GLOBAL_STATE.debt -= 100
            self.notify("Paid $100 (Mocked)")
            self.update_debt_label()
        elif btn_id == "next_assignment":
            self.app.push_screen("map")
