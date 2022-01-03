import toastcord
import asyncio
import sqlite3
import sys
import os

from rich.console import Console

from toastcord.api.types.message import Message

# initialize the database
DB = sqlite3.connect("messages.db")
CURSOR = DB.cursor()

CURSOR.execute(
    "CREATE TABLE IF NOT EXISTS messages "
    "(id INTEGER, message TEXT, author TEXT, timestamp REAL)"
)

DB.commit()


async def index():
    CURSOR.execute("DELETE FROM messages")

    DB.commit()

    async for channel in toastcord.client.channels_async():
        async for message in channel.load_messages():

            if not isinstance(message, Message):
                continue

            CURSOR.execute(
                "INSERT INTO messages VALUES (?, ?, ?, ?)",
                (
                    message.id, message.content,
                    str(message.author), message.timestamp
                )
            )

            DB.commit()

    CURSOR.execute(
        "DELETE FROM messages "
        "WHERE rowid NOT IN (SELECT min(rowid) FROM messages GROUP BY id)"
    )


if __name__ == "__main__":
    token = os.environ.get("DISCORD_TOKEN")
    console = Console()

    if not token:
        console.log("Token: ERROR", style="red")
        sys.exit(1)

    console.log("Token: OK", style="green")

    console.log("Client: OK", style="green")

    console.log("Indexing messages...")
    asyncio.get_event_loop().run_until_complete(index())

    os.system(
        "echo 'SELECT message FROM messages'"
        "|"
        "sqlite3 messages.db"
        "|"
        "fzf -e"
    )

    console.log("Done", style="green")
