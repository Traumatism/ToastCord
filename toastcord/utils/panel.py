from rich.panel import Panel
from rich.box import SQUARE


def get_panel() -> Panel:
    return Panel(
        renderable="",
        box=SQUARE,
        border_style="cyan",
    )
