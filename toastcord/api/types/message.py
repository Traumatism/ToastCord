from dataclasses import dataclass

from .user import User


@dataclass
class Message:
    """ A message """
    id: int
    author: User
    content: str
    timestamp: str
