from typing import Type

from textual.app import App, CSSPathType
from textual.driver import Driver
from textual.events import Mount

from screen.main import Main


class LoaderApp(App[str]):

    # CSS_PATH = "loader.css"
    TITLE = "Loading Reactive List Views"
    SUB_TITLE = ""
    SCREENS = {
        'main': Main
    }

    def __init__(self, driver_class: Type[Driver] | None = None, css_path: CSSPathType | None = None,
                 watch_css: bool = False):
        super().__init__(driver_class, css_path, watch_css)
        import os
        debug_enable = os.environ.get('DEBUG_ENABLE')
        if debug_enable is not None and debug_enable == 'True':
            import pydevd_pycharm
            pydevd_pycharm.settrace('localhost', port=2223, suspend=False)

    def on_mount(self, event: Mount) -> None:
        """App is mounted. Start the Main screen to get things rolling"""
        self.push_screen("main")
