from rich.console import Console

from toastcord.widgets.main import MainWindow
from toastcord import client


if __name__ == "__main__":
    console = Console()

    console.log("Initializing ToastCord client...")

    response = client.initalize()

    if response is False:
        console.log("Failed to initalize client, is the token correct?")
        exit()

    console.log("Client initialized!")

    console.log("Running temrinal UI...")

    MainWindow.run(
        console,
        title="[white]ToastCord[/white]",
    )

    console.log("See ya!")
