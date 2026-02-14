import pytest
import asyncio
from textual.pilot import Pilot
from src.tui.app import BreadBureaucracyApp
from src.tui.screens.shift import ShiftScreen, Counter
from src.tui.screens.menu import MainMenu
from src.tui.screens.map import MapScreen
from src.tui.screens.crisis import CrisisScreen


@pytest.mark.asyncio
async def test_navigation_to_shift_screen():
    """Test navigation from Main Menu to Shift Screen."""
    app = BreadBureaucracyApp()
    async with app.run_test() as pilot:
        await pilot.pause()
        assert isinstance(app.screen, MainMenu)

        await pilot.click("#new_shift")
        await pilot.pause()
        assert isinstance(app.screen, MapScreen)

        await pilot.click("#node-A")
        await pilot.pause()

        assert isinstance(app.screen, ShiftScreen)


@pytest.mark.asyncio
async def test_shift_screen_spawns_customers():
    """Test that the shift screen spawns customers over time."""
    app = BreadBureaucracyApp()

    async with app.run_test() as pilot:
        await app.push_screen("shift")
        await pilot.pause()

        assert isinstance(app.screen, ShiftScreen)

        counter = app.screen.query_one(Counter)
        assert counter.queue_count == 0

        await pilot.pause(1.5)


@pytest.mark.asyncio
async def test_trigger_crisis_from_shift():
    """Test triggering the Crisis Screen from the Shift Screen."""
    app = BreadBureaucracyApp()

    async with app.run_test() as pilot:
        await app.push_screen("shift")
        await pilot.pause()

        assert isinstance(app.screen, ShiftScreen)

        await pilot.press("c")
        await pilot.pause()

        assert isinstance(app.screen, CrisisScreen)
