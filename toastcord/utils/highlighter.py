from rich.highlighter import RegexHighlighter
from rich.theme import Theme


class DiscordHighlighter(RegexHighlighter):
    """ This shit doesn't work. f. """

    base_style = "discord."

    highlights = [
        r"(?P<bold>\*\*.*?\*\*)",
        r"(?P<italic>__.*?__)"
    ]


theme = Theme({
    "discord.code": "green",
    "discord.bold": "bold",
    "discord.italic": "italic"
})
