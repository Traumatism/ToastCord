from dataclasses import dataclass


@dataclass
class ToastyMessage:
    """ A message from Toasty """
    content: str

    def render(self):
        """ Render the message """

        user_color = "red"

        message = f"[{user_color} underline]"
        message += "Toasty"
        message += f"[/{user_color} underline] "
        message += f"\n{self.content}\n"

        return message
