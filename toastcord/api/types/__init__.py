from dataclasses import dataclass


@dataclass
class DiscordObject:
    """ A Discord object """
    id: int  # any Discord object (user, channel, message, etc.) has an id

    def __hash__(self) -> int:
        return self.id

    def __eq__(self, __o: object) -> bool:
        return (
            isinstance(__o, self.__class__)
            and hash(self) == hash(__o)
        )
