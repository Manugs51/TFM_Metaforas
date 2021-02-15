from semantic_source import SemanticSource
import requests


class Babel(SemanticSource):
    def __init__(self, key: str):
        self.__key = key
    
    def find_metaphors(self, words: [(str, str)]) -> str:
        return words[0][0]
