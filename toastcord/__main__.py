from rich.console import Console

from toastcord.widgets.main import MainWindow
from toastcord import client


if __name__ == "__main__":
    console = Console()

    console.log("Initializing client...")

    response = client.initalize()

    if response is False:
        console.log("Failed to initalize client, is the token correct?")
        exit()

    console.log("Initalized client, starting window manager...")

    MainWindow.run(
        console,
        title="[white]ToastCord[/white]",
    )

    console.log("See ya!")
