from rich.panel import Panel
from rich.box import ROUNDED


def get_panel() -> Panel:

    return Panel(
        renderable="",
        box=ROUNDED,
        border_style="cyan"
    )
