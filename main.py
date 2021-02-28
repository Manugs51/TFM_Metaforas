from secrets import secrets
from babel_categories import BabelCategories
from babel_lemmas_of_senses import BabelLemmasOfSenses
from babel_parser import BabelParser



def get_text() -> str:
    return input()

def show_metaphors(text:str) -> None:
    print(text)
    pass

if __name__ == '__main__':
    source = BabelCategories(secrets['babel_key'])
    parser = BabelParser(secrets['babel_key'])
    while True:
        text = get_text()
        word_and_id = parser.parse(text)
        print(word_and_id)
        metaphors_found = source.find_metaphors(word_and_id)
        show_metaphors(metaphors_found)
