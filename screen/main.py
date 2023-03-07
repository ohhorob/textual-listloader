import asyncio
import random
import string
from asyncio import sleep

from rich.console import RenderableType
from rich.text import Text
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Container
from textual.events import Mount
from textual.reactive import reactive
from textual.screen import Screen
from textual.widgets import Static, Header, Footer

from widget.loadable import LoadableListView


class Body(Container):
    pass


class LengthLabel(Static):
    length = reactive(0, layout=True)

    def render(self) -> RenderableType:
        """Something silly like a vampire multiplied by length"""
        return Text.from_markup(" ".join([":vampire:" for i in range(0, self.length)]))



class Main(Screen):

    CSS_PATH = "main.css"

    BINDINGS = [
        Binding("escape", "quit", "Close"),
        Binding("k", "remvalue", "Remove value", show=True),
        Binding("l", "addvalue", "Add value", show=True)
    ]

    # I'd prefer the values be owned by the screen
    # controls/bindings/actions can manipulate the collection and ListView widget is just displaying it
    # values: set = reactive(set(), layout=True)

    def __init__(
            self,
            name: str | None = None,
            id: str | None = None,
            classes: str | None = None,
    ):
        super().__init__(name, id, classes)
        # these initial values aren't rendered correctly
        # self.options = LoadableListView(initial_values={'one', 'two', 'three'})
        self.options = LoadableListView()
        self.len_label = LengthLabel()
        self.len_label.length = 0

    async def load_itemdata(self) -> None:
        """Spend some time loading values to display"""
        values = set()
        for i in range(1, 5):
            values.add(str(i))
        await sleep(5.0)
        self.options.values = set(values)

    def on_mount(self, event: Mount) -> None:
        """Screen is composed of Widgets

        This is syncronous and before rendering. Not a good place to spend time
        """
        asyncio.create_task(self.load_itemdata())

    def action_addvalue(self) -> None:
        # reactive attribute is not being watched unless changing the assignment
        # self.options.values.add('blah') doesn't work
        value = random.choice(string.ascii_letters) * int(random.uniform(2, 8))
        if self.options.values:
            self.options.values = {s for s in (*self.options.values, value)}
        else:
            self.options.values = {value}

        # also give the length label a nudge
        self.query_one(LengthLabel).length = len(self.options.values)

    def action_remvalue(self) -> None:
        # self.options.values.pop() doesn't work; have to re-create the set
        if len(self.options.values) > 0:
            result = self.options.values.copy()
            result.pop()
            self.options.values = result

            # also give the length label a nudge
            self.query_one(LengthLabel).length = len(self.options.values)

    def compose(self) -> ComposeResult:
        yield Container(
            Header(show_clock=True),
            Body(
                self.len_label,
                Static("Value List"),
                self.options,
            )
        )
        yield Footer()
