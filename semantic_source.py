import abc

class SemanticSource(metaclass=abc.ABCMeta):
    
    @abc.abstractmethod
    def find_metaphors(self, words: [(str, str)]) -> str:
        return None
