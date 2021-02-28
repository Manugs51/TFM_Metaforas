from semantic_source import SemanticSource
from babel_html_api import api
import requests


class BabelCategories(SemanticSource):
    def __init__(self, key: str):
        key_part = '?key=' + key
        incomplete_synset_part = '&id='
        self.complete_url = api['information_given_synset_url'] + key_part + incomplete_synset_part

    #TODO this does not take @words
    def find_metaphors(self, words: [(str, str)]) -> str:
        #list of jsons containing categories
        info_of_synsets_response = [requests.get(self.complete_url+w[1]).json() for w in words]
        #list of list of json categories
        categories_of_words = [w['categories'] for w in info_of_synsets_response]
        #list of list of categories
        category_names_of_words = [list(map(lambda elem : elem['category'], c)) for c in categories_of_words]
        #TODO refactor
        cat1 = sorted(category_names_of_words[0])
        cat2 = sorted(category_names_of_words[2])
        print(cat1)
        print(cat2)
        ret = 'hay metáfora'
        for c in cat1:
            if c in cat2:
                ret = 'no hay metáfora'
                print(c)
        return ret
