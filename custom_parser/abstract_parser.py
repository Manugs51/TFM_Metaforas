import abc
from typing import List, Tuple


class Parser(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def parse(self, text: str) -> List[Tuple[str, str]]:
        return None

    @abc.abstractmethod
    def toString(self) -> str:
        return None
