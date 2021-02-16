import abc

class MyParser(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def parse(self, text: str) -> [(str, str)]:
        return None
