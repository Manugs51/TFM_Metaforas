from semantic_source import SemanticSource
from babel_html_api import api
import requests


class BabelLemmasOfSenses(SemanticSource):
    def __init__(self, key: str):
        key_part = '?key=' + key
        lang_part = '&' + api['search_spanish']
        incomplete_lemma_part = '&lemma='
        self.complete_url = api['senses_given_word_url'] + key_part + lang_part + incomplete_lemma_part

    def find_metaphors(self, words: [(str, str)]) -> str:
        #list of lists of jsons
        synsets_of_words_response = [requests.get(self.complete_url+w[0]).json() for w in words]
        #list of lists of ids
        #print([list(map(lambda elem : elem['properties']['simpleLemma'], s)) for s in synsets_of_words_response])
        synsets_of_words = [list(map(lambda elem : elem['properties']['simpleLemma'], s)) 
                            for s in synsets_of_words_response]
        #TODO refactor
        noun1 = sorted(synsets_of_words[0])
        print(noun1)
        noun2 = sorted(synsets_of_words[2])
        print(noun2)
        ret = 'hay metáfora'
        for syn in noun1:
            if syn in noun2:
                ret = 'no hay metáfora'
                print(syn)
        print(ret)
        return ret
