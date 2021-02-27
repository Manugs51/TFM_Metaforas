from secrets import secrets
from babel import Babel
from babel_parser import BabelParser



def get_text() -> str:
    return input()

def show_metaphors(text:str) -> None:
    print(text)
    pass

if __name__ == '__main__':
    source = Babel(secrets['babel_key'])
    parser = BabelParser(secrets['babel_key'])
    while True:
        text = get_text()
        parsed_text = parser.parse(text)
        print(parsed_text)
        metaphors_found = source.find_metaphors_like_TFG(parsed_text)
        show_metaphors(metaphors_found)
