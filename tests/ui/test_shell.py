import pytest
from textual.pilot import Pilot
from textual.widgets import Button

# Import the application under test
from src.tui.app import BreadBureaucracyApp
from src.tui.screens.menu import MainMenu
from src.tui.screens.settings import SettingsScreen


@pytest.mark.asyncio
async def test_app_starts_at_main_menu():
    """Test that the application launches directly into the Main Menu."""
    app = BreadBureaucracyApp()
    async with app.run_test() as pilot:
        await pilot.pause()
        assert isinstance(app.screen, MainMenu)
        assert str(app.screen.query_one("#new_shift", Button).label) == "New Shift"
        assert str(app.screen.query_one("#settings", Button).label) == "Settings"
        assert str(app.screen.query_one("#quit", Button).label) == "Quit"


@pytest.mark.asyncio
async def test_navigation_settings_and_back():
    """Test navigation from Main Menu to Settings and back."""
    app = BreadBureaucracyApp()
    async with app.run_test() as pilot:
        await pilot.pause()

        assert isinstance(app.screen, MainMenu)

        await pilot.click("#settings")
        await pilot.pause()

        assert isinstance(app.screen, SettingsScreen)
        assert str(app.screen.query_one("#back", Button).label) == "Back"

        await pilot.click("#back")
        await pilot.pause()

        assert isinstance(app.screen, MainMenu)


@pytest.mark.asyncio
async def test_quit_button():
    """Test that clicking Quit exits the application."""
    app = BreadBureaucracyApp()
    async with app.run_test() as pilot:
        await pilot.pause()
        assert app.is_running

        await pilot.click("#quit")
        await pilot.pause()

        assert not app.is_running
