import pytest
import os
from pathlib import Path
from textual.widgets import Label, Button
from src.tui.app import BreadBureaucracyApp
from src.tui.screens.menu import MainMenu
from src.tui.screens.map import MapScreen
from src.tui.screens.shift import ShiftScreen
from src.tui.screens.settlement import SettlementScreen
from src.tui.screens.testing import TestingScreen
from src.tui.state import GLOBAL_STATE

SAVE_FILE = Path("savegame.json")


@pytest.mark.asyncio
async def test_game_loop_flow():
    """
    Verifies the full game loop:
    Menu -> (New Shift) -> Map -> (Select Node) -> Shift -> (End Shift) -> Settlement -> (Next Assignment) -> Map
    """
    # Cleanup before test
    if SAVE_FILE.exists():
        os.remove(SAVE_FILE)

    app = BreadBureaucracyApp()
    async with app.run_test() as pilot:
        assert isinstance(app.screen, MainMenu)

        assert app.screen.query("#new_shift")
        assert app.screen.query("#resume_shift")
        assert not app.screen.query("#map")
        assert not app.screen.query("#settlement")

        await pilot.click("#new_shift")
        await pilot.pause()

        assert isinstance(app.screen, MapScreen)

        await pilot.click("#node-A")
        await pilot.pause()

        assert isinstance(app.screen, ShiftScreen)

        await pilot.click("#end_shift")
        await pilot.pause()

        assert isinstance(app.screen, SettlementScreen)

        await pilot.click("#next_assignment")
        await pilot.pause()

        assert isinstance(app.screen, MapScreen)

    if SAVE_FILE.exists():
        os.remove(SAVE_FILE)


@pytest.mark.asyncio
async def test_testing_screen_navigation():
    """
    Verifies navigation to the Testing screen from Main Menu.
    """
    app = BreadBureaucracyApp()
    async with app.run_test() as pilot:
        assert isinstance(app.screen, MainMenu)

        # Check for Testing button
        assert app.screen.query("#testing_btn")

        await pilot.click("#testing_btn")
        await pilot.pause()

        # Verify we are on TestingScreen
        assert isinstance(app.screen, TestingScreen)

        # Verify we can go back
        await pilot.click("#back_btn")
        await pilot.pause()

        assert isinstance(app.screen, MainMenu)
