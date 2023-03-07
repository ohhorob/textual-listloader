import random
import string
from time import sleep
from typing import Set, Callable, TypeVar

from rich.console import RenderableType
from rich.text import Text
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Container
from textual.reactive import reactive
from textual.screen import Screen
from textual.widgets import Static, Header, Footer, ListView, ListItem


class Body(Container):
    pass


class LengthLabel(Static):
    length = reactive(0, layout=True)

    def render(self) -> RenderableType:
        """Something silly like a vampire multiplied by length"""
        return Text.from_markup(" ".join([":vampire:" for i in range(0, self.length)]))


T = TypeVar("T")


class LoadableListView(ListView):
    """Idea is to match your value type with an item factory to dynamically create items from values

    The values are reactive, casing new items to be added and old to be removed. This is keyed by the item name.
    Some better strategy for auto-naming is probably needed for this to be reusable.
    """

    # Replace this set to re-draw the items in the list
    values: Set[T] = reactive(set(), layout=False, init=False)

    def __init__(
            self,
            item_factory: Callable[[T], ListItem] | None = None,
            initial_values: set | None = None,
            initial_index: int | None = 0,
            name: str | None = None,
            id: str | None = None,
            classes: str | None = None,
            disabled: bool = False
    ) -> None:
        super().__init__(initial_index=initial_index, name=name, id=id, classes=classes, disabled=disabled)
        if item_factory is not None:
            self._item_factory = item_factory
        else:
            self._item_factory = lambda v: ListItem(Static(str(v)), name=str(v))
        self.values = initial_values

    def watch_values(self, old: Set[T], now: Set[T]):
        # Attempt: update ListView with item changes
        for v in now.difference(old):
            self.append(self._item_factory(v))

        remove_names: Set[T] = {str(v) for v in old.difference(now)}
        if len(remove_names) > 0:
            for i in self.children:
                if i.name in remove_names:
                    i.remove()


def load_itemdata() -> Set[str]:
    """Spend some time loading values to display"""
    values = set()
    for i in range(1, 5):
        values.add(str(i))
    sleep(2.0)
    return set(values)


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
        self.options = LoadableListView(initial_values={'one', 'two', 'three'})
        self.len_label = LengthLabel()
        self.len_label.length = len(self.options.values)

    def on_resume(self) -> None:
        if len(self.options.values) == 0:
            self.options.values = load_itemdata()

    def action_loadvalues(self):
        self.options.values = load_itemdata()

    def action_addvalue(self) -> None:
        # reactive attribute is not being watched unless changing the assignment
        # self.options.values.add('blah') doesn't work
        value = random.choice(string.ascii_letters) * int(random.uniform(2, 8))
        self.options.values = {s for s in (*self.options.values, value)}
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
