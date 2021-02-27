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
        
        info_of_synsets_response = [requests.get(self.complete_url+w[0]).json() for w in words]
        
        return 'TODO'
