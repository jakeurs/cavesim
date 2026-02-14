import pytest
from textual.widgets import ListView, ProgressBar
from src.tui.app import BreadBureaucracyApp
from src.tui.screens.crisis import CrisisScreen
from src.models.content import Decree
from src.models.enums import CookingMethod


@pytest.mark.asyncio
async def test_crisis_screen_initialization():
    """Test that the Crisis Screen initializes correctly."""
    app = BreadBureaucracyApp()

    decree = Decree(
        id="test_decree",
        target_tag="dough",
        operation=CookingMethod.LAMINATE,
        requirements=[
            {"type": "stat_gt", "stat": "elasticity", "value": 50, "token_key": "val"}
        ],
        text_template="Elasticity must be above {val}.",
        token_keys={"val": "value"},
        success_effect="compliment",
        failure_effect="insult",
    )

    screen = CrisisScreen(decree=decree)

    async with app.run_test() as pilot:
        await app.push_screen(screen)
        await pilot.pause()

        assert isinstance(app.screen, CrisisScreen)
        assert app.screen.query_one(ListView)
        assert app.screen.query_one(ProgressBar)


@pytest.mark.asyncio
async def test_crisis_screen_interaction():
    """Test selecting options in the Crisis Screen."""
    app = BreadBureaucracyApp()

    decree = Decree(
        id="test_decree",
        target_tag="dough",
        operation=CookingMethod.LAMINATE,
        requirements=[
            {"type": "stat_gt", "stat": "elasticity", "value": 50, "token_key": "val"}
        ],
        text_template="Elasticity must be above {val}.",
        token_keys={"val": "value"},
        success_effect="compliment",
        failure_effect="insult",
    )

    screen = CrisisScreen(decree=decree)

    async with app.run_test() as pilot:
        await app.push_screen(screen)
        await pilot.pause()

        # Verify question is displayed (implied by ListView having items)
        list_view = app.screen.query_one(ListView)
        assert len(list_view.children) > 0

        await pilot.press("enter")
        await pilot.pause()


@pytest.mark.asyncio
async def test_crisis_logic():
    """Test the game logic: rage meter and answer checking."""
    app = BreadBureaucracyApp()

    decree = Decree(
        id="test_decree",
        target_tag="dough",
        operation=CookingMethod.LAMINATE,
        requirements=[
            {"type": "stat_gt", "stat": "elasticity", "value": 50, "token_key": "val"}
        ],
        text_template="Elasticity must be above {val}.",
        token_keys={"val": "value"},
        success_effect="compliment",
        failure_effect="insult",
    )

    screen = CrisisScreen(decree=decree)

    async with app.run_test() as pilot:
        await app.push_screen(screen)
        await pilot.pause()

        initial_rage = screen.rage
        await pilot.pause(1.1)
        assert screen.rage > initial_rage

        correct = screen.question_data["answer"]
        options = screen.question_data["options"]
        wrong_index = -1
        for i, opt in enumerate(options):
            if opt != correct:
                wrong_index = i
                break

        list_view = screen.query_one(ListView)
        list_view.index = wrong_index
        await pilot.press("enter")
        await pilot.pause()

        assert screen.rage >= initial_rage + 20

        correct_index = options.index(correct)
        list_view.index = correct_index
        await pilot.press("enter")
        await pilot.pause()

        assert not isinstance(app.screen, CrisisScreen)
