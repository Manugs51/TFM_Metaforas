from my_parser import MyParser
from babel_html_api import api
import requests
import tags


class BabelParser(MyParser):
    def __init__(self, key: str):
        key_part = '?key=' + key
        lang_part = '&' + api['spanish']
        incomplete_text_part = '&text='
        self.complete_url = api['disambiguate_url'] + key_part + lang_part + incomplete_text_part
    
    #TODO: convertir a minusculas, babel tiene problemas con ES
    def parse(self, text: str) -> [(str, str)]:
        r = requests.get(self.complete_url+text)
        # For synsets in json return the word (start->end) + sysnsetID
        return [
                (text[elem['charFragment']['start'] : elem['charFragment']['end']+1],
                elem['babelSynsetID'])
            for elem in r.json()]
    
    def toString(self) -> str:
        return 'babel_parser'
