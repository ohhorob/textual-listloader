from typing import Set, Callable, TypeVar

from textual.reactive import reactive
from textual.widgets import ListView, ListItem, Static


T = TypeVar("T")


class LoadableListView(ListView):
    """Idea is to match your value type with an item factory to dynamically create items from values

    The values are reactive, casing new items to be added and old to be removed. This is keyed by the item name.
    Some better strategy for auto-naming is probably needed for this to be reusable.
    """

    # Replace this set to re-draw the items in the list
    values: Set[T] | None = reactive(None, layout=False, init=False)

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
        if initial_values is not None:
            self.values = initial_values

    def watch_values(self, old: Set[T], now: Set[T]):
        # Attempt: update ListView with item changes
        for v in now.difference(old) if old else now:
            self.append(self._item_factory(v))

        if old:
            remove_names: Set[T] = {str(v) for v in old.difference(now)}
            if len(remove_names) > 0:
                for i in self.children:
                    if i.name in remove_names:
                        i.remove()
