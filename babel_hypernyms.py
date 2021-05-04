from semantic_source import SemanticSource
from babel_html_api import api
import requests


class BabelHypernyms(SemanticSource):
    def __init__(self, key: str):
        key_part = '?key=' + key
        incomplete_synset_part = '&id='
        self.complete_url = api['edges_given_synset_url'] + key_part + incomplete_synset_part

    def find_metaphors(self, words: [(str, str)]) -> str:
        #list of jsons containing edges
        edges_of_synsets_response = [requests.get(self.complete_url+w[1]).json() for w in words]
        #list of lists of json containing hypernym links
        hypernyms_of_words = [list(filter(lambda elem : elem['pointer']['relationGroup'] == 'HYPERNYM', edges)) for edges in edges_of_synsets_response]
        #list of lists of ids of hypernyms
        ids_of_hypernyms = [list(map(lambda edge : edge['target'], h)) for h in hypernyms_of_words]
        #TODO refactor
        hyp1 = set(ids_of_hypernyms[0])
        hyp2 = set(ids_of_hypernyms[2])
        print(hyp1)
        print(hyp2)
        ret = 'hay metáfora'
        for h in hyp2:
            if words[2][1] == h['target']:
                ret = 'no hay metáfora'
                print(h)
        return ret

    def toString(self) -> str:
        return 'babel_hypernyms'
