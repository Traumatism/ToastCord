from dataclasses import dataclass


@dataclass
class User:
    """ A Discord user """
    id: int
    username: str
    discriminator: int

    def __eq__(self, __o: "User") -> bool:
        return self.id == __o.id

    def __str__(self) -> str:
        return f"{self.username}#{self.discriminator}"
