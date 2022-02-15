from rich.panel import Panel
from rich.box import ROUNDED


def get_panel() -> Panel:
    """ Get a panel base """
    return Panel(
        renderable="",
        box=ROUNDED,
        border_style="cyan",
        highlight=True,
    )
