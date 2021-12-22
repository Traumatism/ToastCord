from abc import ABC, abstractmethod

from typing import Any


class ToastCordScript(ABC):
    """ ToastCord script base class """

    class ToastCordMessage:
        """ ToastCord API message """

        def __init__(self, target: Any) -> None:
            self.target = target

    def __init__(self) -> None:
        pass

    @abstractmethod
    async def on_message(self, message: ToastCordMessage) -> None:
        """ This method is called when a message is received """

    @abstractmethod
    async def run(self) -> None:
        """ This method will contains script code """
