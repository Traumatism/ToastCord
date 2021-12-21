from datetime import datetime

from rich.console import RenderableType
from rich.table import Table

from textual.widget import Widget

from toastcord import client, version
from toastcord.utils.panel import get_panel


class Header(Widget):

    def render(self) -> RenderableType:

        table = Table.grid(padding=(0, 1), expand=True)

        table.add_column(justify="left", ratio=0, width=20)
        table.add_column("title", justify="center", ratio=20)
        table.add_column("clock", justify="right", width=20)

        table.add_row(
            str(client.user), f"[italic]ToastCord v{version}[/italic]",
            datetime.now().time().strftime("%X")
        )

        panel = get_panel()
        panel.renderable = table

        return panel

    async def on_mount(self, event) -> None:
        self.set_interval(1.0, callback=self.refresh)
