from my_parser import MyParser
import requests


class BabelParser(MyParser):
    def __init__(self, key: str):
        self.__key = key
    
    def parse(self, text: str) -> [(str, str)]:
        return [(word,'TODO') for word in text.split()]
