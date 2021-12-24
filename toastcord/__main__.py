import toastcord

from rich.console import Console

from toastcord.utils.highlighter import theme
from toastcord.widgets.main import MainWindow

if __name__ == "__main__":
    console = Console(theme=theme)

    console.log("Initializing ToastCord client...")

    response = toastcord.client.initalize()

    if response is False:
        console.log("Failed to initalize client, is the token correct?")
        exit()

    console.log(f"Client initialized! Logged in as {toastcord.client.user}")

    console.log("Running terminal UI...")

    MainWindow.run(console=console)

    console.log("See ya!")
