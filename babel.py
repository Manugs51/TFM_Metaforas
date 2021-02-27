from semantic_source import SemanticSource
from babel_html_api import api
import requests


class Babel(SemanticSource):
    def __init__(self, key: str):
        self.complete_url = api['information_given_synset_url'] + '?key=' + key + '&' + api['buscar_español'] + '&lemma='
        self.complete_url_tfg = api['senses_given_word_url'] + '?key=' + key + '&' + api['buscar_español'] + '&lemma='

    def find_metaphors(self, words: [(str, str)]) -> str:
        #list of lists of jsons
        synsets_of_words_response = [requests.get(self.complete_url+w[0]).json() for w in words]
        #list of lists of ids
        #print([list(map(lambda elem : elem['properties']['simpleLemma'], s)) for s in synsets_of_words_response])
        synsets_of_words = [list(map(lambda elem : elem['properties']['simpleLemma'], s)) for s in synsets_of_words_response]
        #TODO refactor
        noun1 = synsets_of_words[0]
        print(noun1)
        noun2 = synsets_of_words[2]
        print(noun1)
        ret = 'hay metáfora'
        for syn in noun1:
            if syn in noun2:
                ret = 'no hay metáfora'
        for syn in noun2:
            if syn in noun1:
                ret = 'no hay metáfora'
        print(ret)
        return ret
    
    def find_metaphors_like_TFG(self, words: [(str, str)]) -> str:
        #list of lists of jsons
        synsets_of_words_response = [requests.get(self.complete_url_tfg+w[0]).json() for w in words]
        #list of lists of ids
        #print([list(map(lambda elem : elem['properties']['simpleLemma'], s)) for s in synsets_of_words_response])
        synsets_of_words = [list(map(lambda elem : elem['properties']['simpleLemma'], s)) for s in synsets_of_words_response]
        #TODO refactor
        noun1 = synsets_of_words[0]
        print(noun1)
        noun2 = synsets_of_words[2]
        print(noun1)
        ret = 'hay metáfora'
        for syn in noun1:
            if syn in noun2:
                ret = 'no hay metáfora'
        for syn in noun2:
            if syn in noun1:
                ret = 'no hay metáfora'
        print(ret)
        return ret
