from textual.screen import Screen
from textual.widgets import ListView, ProgressBar, Label, ListItem
from textual.containers import Container
from textual.app import ComposeResult
from textual import on
from src.models.content import Decree
from src.engine.decree import generate_question


class CrisisScreen(Screen):
    CSS = """
    CrisisScreen {
        align: center middle;
    }
    #rage_meter {
        width: 80%;
        margin: 1;
    }
    ListView {
        width: 80%;
        height: 60%;
        border: solid red;
    }
    """

    def __init__(self, decree: Decree, **kwargs):
        super().__init__(**kwargs)
        self.decree = decree
        self.rage = 0
        self.question_data = generate_question(decree)
        self.timer = None

    def compose(self) -> ComposeResult:
        yield Label(self.question_data["question"])
        yield ProgressBar(total=100, show_eta=False, id="rage_meter")

        items = [ListItem(Label(opt)) for opt in self.question_data["options"]]
        yield ListView(*items)

    def on_mount(self) -> None:
        self.timer = self.set_interval(0.1, self.tick)

    def tick(self) -> None:
        self.rage += 1
        self.update_meter()
        if self.rage >= 100:
            self.game_over()

    def update_meter(self) -> None:
        meter = self.query_one(ProgressBar)
        meter.progress = self.rage

    @on(ListView.Selected)
    def check_answer(self, event: ListView.Selected) -> None:
        list_view = self.query_one(ListView)
        index = list_view.index
        if index is None:
            return

        selected_text = self.question_data["options"][index]

        if selected_text == self.question_data["answer"]:
            self.dismiss(result=True)
        else:
            self.rage += 20
            self.update_meter()

    def game_over(self) -> None:
        self.dismiss(result=False)
