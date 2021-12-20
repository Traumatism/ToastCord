from rich.console import Console

from toastcord.widgets.main import MainWindow
from toastcord import client


if __name__ == "__main__":
    console = Console()
    client.initalize()

    MainWindow.run(
        console,
        title="[white]ToastCord[/white]",
    )
