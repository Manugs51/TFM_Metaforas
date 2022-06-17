from typing import List, Tuple
from links.babel_html_api import api # pylint: disable=import-error
import requests
from custom_parser.abstract_parser import Parser # pylint: disable=import-error


class BabelParser(Parser):
    def __init__(self, key: str):
        key_part = '?key=' + key
        lang_part = '&' + api['spanish']
        incomplete_text_part = '&text='
        self.complete_url = api['disambiguate_url'] + key_part + lang_part + incomplete_text_part
    
    #TODO: convertir a minusculas, babel tiene problemas con ES
    def parse(self, text: str) -> List[Tuple[str, str]]:
        r = requests.get(self.complete_url+text)
        # For synsets in json return the word (start->end) + sysnsetID
        return [
                (text[elem['charFragment']['start'] : elem['charFragment']['end']+1],
                elem['babelSynsetID'])
            for elem in r.json()]
    
    def toString(self) -> str:
        return 'babel_parser'
