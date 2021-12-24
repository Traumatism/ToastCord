from dataclasses import dataclass


@dataclass
class ToastyMessage:
    """ A message from Toasty """
    content: str
