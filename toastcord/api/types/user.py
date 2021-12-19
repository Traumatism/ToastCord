from dataclasses import dataclass


@dataclass
class User:
    """ A Discord user """
    id: int
    username: str
    discriminator: str

    selected: bool = False

    def __eq__(self, __o: "User") -> bool:
        return self.id == __o.id

    def __str__(self) -> str:
        selection_indicator = ' > ' if self.selected is True else ''

        return f"{selection_indicator}{self.username}#{self.discriminator}"
