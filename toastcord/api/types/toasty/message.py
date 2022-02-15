from dataclasses import dataclass


@dataclass
class ToastyMessage:
    """ A message from Toasty """
    content: str

    def render(self) -> str:
        """ Render the message """
        return f"[red underline]Toasty[/red underline]\n{self.content}\n"
