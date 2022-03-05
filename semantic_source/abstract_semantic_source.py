import abc
from typing import List, Tuple

class SemanticSource(metaclass=abc.ABCMeta):
    
    @abc.abstractmethod
    def find_metaphors(self, words: List[Tuple[str, str]]):
        return None
    
    @abc.abstractmethod
    def toString(self) -> str:
        return None
    
    def subject(self, words: List[Tuple[str, str]]) -> Tuple[str, str]:
        return words[0]
    
    def attribute(self, words: List[Tuple[str,str]]) -> Tuple[str, str]:
        return words[2]
