from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Header, Footer, Static, Button
from textual.containers import Vertical, Horizontal, Center
from textual.reactive import reactive
from src.tui.screens.crisis import CrisisScreen
from src.models.content import Decree
from src.models.enums import CookingMethod


class Counter(Static):
    queue_count = reactive(0)

    def watch_queue_count(self, count: int) -> None:
        self.refresh()

    def render(self) -> str:
        return f"Queue: {self.queue_count}"


class Kitchen(Static):
    def render(self) -> str:
        return "Kitchen: Ovens Ready"


class ShiftScreen(Screen):
    BINDINGS = [("c", "trigger_crisis", "Trigger Crisis")]
    customer_count = reactive(0)

    def compose(self) -> ComposeResult:
        yield Header()
        yield Horizontal(
            Counter(id="counter"),
            Kitchen(id="kitchen"),
        )
        yield Center(Button("End Shift", id="end_shift"))
        yield Footer()

    def on_mount(self) -> None:
        self.set_interval(1.0, self.spawn_customer)

    def spawn_customer(self) -> None:
        self.customer_count += 1

    def watch_customer_count(self, count: int) -> None:
        try:
            self.query_one(Counter).queue_count = count
        except Exception:
            pass

    def action_trigger_crisis(self) -> None:
        decree = Decree(
            id="random_crisis",
            target_tag="dough",
            operation=CookingMethod.LAMINATE,
            requirements=[
                {
                    "type": "stat_gt",
                    "stat": "elasticity",
                    "value": 50,
                    "token_key": "val",
                }
            ],
            text_template="Elasticity must be above {val}.",
            token_keys={"val": "value"},
            success_effect="compliment",
            failure_effect="insult",
        )
        self.app.push_screen(CrisisScreen(decree=decree))

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "end_shift":
            self.app.push_screen("settlement")
