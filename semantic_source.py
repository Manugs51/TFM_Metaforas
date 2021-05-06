import abc

class SemanticSource(metaclass=abc.ABCMeta):
    
    @abc.abstractmethod
    def find_metaphors(self, words: [(str, str)]):
        return None
    
    @abc.abstractmethod
    def toString(self) -> str:
        return None
    
    def subject(self, words: [(str, str)]) -> (str, str):
        return words[0]
    
    def attribute(self, words: [(str,str)]) -> (str, str):
        return words[2]
