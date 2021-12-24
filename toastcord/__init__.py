# fuck pep8

import argparse

VERSION = "1.0.0"

parser = argparse.ArgumentParser()

parser.add_argument(
    "-t", "--token",
    required=True,
    help="Your Discord API token",
    dest="token",
    metavar="<value>"
)

http_options = parser.add_argument_group("HTTP Options")

http_options.add_argument(
    "--user-agent",
    default=f"toastcord_love_discord_t0s/{VERSION}",
    help="User-Agent header",
    dest="user_agent",
    metavar="<value>"
)

api_options = parser.add_argument_group("Discord API options")

api_options.add_argument(
    "--api-backend",
    default="https://canary.discord.com/api/",
    help="Discord API backend to use",
    dest="api_backend",
    metavar="<value>"
)

api_options.add_argument(
    "--api-version",
    default="v9",
    help="Discord API version to use",
    dest="api_version",
    metavar="<value>"
)

arguments = parser.parse_args()

API_VERSION = arguments.api_version
API_BACKEND = arguments.api_backend
USER_AGENT = arguments.user_agent
TOKEN = arguments.token

from .api.client import Client

client = Client()

WELCOME_SCREEN = """[blue][bold]
 ╔╦╗╔═╗╔═╗╔═╗╔╦╗ [white]┌─┐┌─┐┬─┐┌┬┐[/white]
  ║ ║ ║╠═╣╚═╗ ║  [white]│  │ │├┬┘ ││[/white]
  ╩ ╚═╝╩ ╩╚═╝ ╩  [white]└─┘└─┘┴└┘└┴┘[/white]
[/blue][/bold]

  Discord client for nerds
  Developed by [magenta]toast#3108[/magenta]

  Mail      > cpastoast@protonmail.com
  Telegram  > toastakerman
  GitHub    > traumatism
  Twitter   > toastakerman

  This is a beta version. Bug reports and feature requests
  are welcome at @toastakerman.

  This might be agains't the Discord TOS,
  see https://discord.com/terms.

  This is still being developed. Don't forget to [code]git fetch[/code]
  and [code]git pull[/code] regularly.

  Keybinds:
    - r > Refresh the messages in the selected channel
    - s > Toggle the sidebar
    - q > Exit ToastCord

"""
