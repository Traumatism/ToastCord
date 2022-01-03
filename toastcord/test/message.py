from rich import print

from rich.text import Text


content = """Hi,
My name is Victor and i am 15 years old.

Thanks for reading :D
thatstringiskindalongthatstringiskindalongthatstringiskindalongthatstringin"""


def make_box(content: str):

    x = max(len(line) for line in content.split("\n"))

    _content = "".join(
        f"  {line}{' ' * (x - len(line))}  \n"
        for line in content.split("\n")
    )

    hc = Text("▄▄", "cyan")
    fc = Text("▀▀", "cyan")
    line = Text(" " * x, "black on cyan")

    rcontent = Text(_content, "black on cyan")

    return Text.assemble(hc, line, hc, "\n", rcontent, fc, line, fc)


print(make_box(content))
