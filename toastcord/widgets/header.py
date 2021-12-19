from datetime import datetime

from rich.console import RenderableType
from rich.table import Table

from textual import events
from textual.widget import Widget
from textual.reactive import Reactive

from toastcord import client
from toastcord.utils.panel import get_panel


class Header(Widget):
    def __init__(self) -> None:
        super().__init__()

    tall: Reactive[bool] = Reactive(True, layout=True)

    @property
    def full_title(self) -> str:
        return f"ToastCord ({client.user})"

    def render(self) -> RenderableType:
        header_table = Table.grid(padding=(0, 1), expand=True)
        header_table.style = self.style
        header_table.add_column(justify="left", ratio=0, width=8)
        header_table.add_column("title", justify="center", ratio=1)
        header_table.add_column("clock", justify="right", width=8)

        header_table.add_row(
            "👾", self.full_title, datetime.now().time().strftime("%X")
        )

        panel = get_panel()
        panel.renderable = header_table

        return panel

    async def on_mount(self, event: events.Mount) -> None:
        self.set_interval(1.0, callback=self.refresh)
