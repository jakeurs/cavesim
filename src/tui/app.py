from textual.app import App
from src.tui.screens.menu import MainMenu
from src.tui.screens.settings import SettingsScreen
from src.tui.screens.shift import ShiftScreen
from src.tui.screens.map import MapScreen
from src.tui.screens.settlement import SettlementScreen
from src.tui.screens.testing import TestingScreen


class BreadBureaucracyApp(App):
    TITLE = "Bread & Bureaucracy"
    CSS = """
    Screen {
        layout: vertical;
    }
    """

    SCREENS = {
        "menu": MainMenu,
        "settings": SettingsScreen,
        "shift": ShiftScreen,
        "map": MapScreen,
        "settlement": SettlementScreen,
        "testing": TestingScreen,
    }

    def on_mount(self) -> None:
        self.push_screen("menu")


if __name__ == "__main__":
    app = BreadBureaucracyApp()
    app.run()
