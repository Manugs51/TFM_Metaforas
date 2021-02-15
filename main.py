from secrets import secrets
from babel import Babel
from babel_parser import BabelParser

def get_text() -> str:
    return input()

def show_metaphors(text:str) -> None:
    print(text)
    pass

if __name__ == '__main__':
    source = Babel(secrets['babel_net_key'])
    parser = BabelParser(secrets['babel_net_key'])
    while True:
        text = get_text()
        parsed_text = parser.parse(text)
        metaphors_found = source.find_metaphors(parsed_text)
        show_metaphors(metaphors_found)
