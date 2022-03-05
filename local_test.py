from secrets import secrets
from semantic_source.babel_categories import BabelCategories
from semantic_source.babel_hypernyms import BabelHypernyms
from semantic_source.babel_lemmas_of_senses import BabelLemmasOfSenses
from custom_parser.babel_parser import BabelParser



def get_text() -> str:
    return input()

def show_metaphors(text:str) -> None:
    print(text)
    pass

if __name__ == '__main__':
    source = BabelLemmasOfSenses(secrets['babel_key'])
    parser = BabelParser(secrets['babel_key'])
    while True:
        text = get_text()
        word_and_id = parser.parse(text)
        print(word_and_id)
        metaphors_found = source.find_metaphors(word_and_id)
        show_metaphors(metaphors_found)
