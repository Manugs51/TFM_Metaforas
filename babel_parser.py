from my_parser import MyParser
from babel_html_api import api
import requests
import tags


class BabelParser(MyParser):
    def __init__(self, key: str):
        self.complete_url = api['disambiguate_url'] + '?key=' + key + '&' + api['español'] + '&text='
    
    def parse(self, text: str) -> [(str, str)]:
        r = requests.get(self.complete_url+text)
        # For synsets in jason return the word (start->end) + type of word (last char of sysnsetID)
        return [
                (text[elem['charFragment']['start'] : elem['charFragment']['end']+1],
                tags.BABEL[elem['babelSynsetID'][-1]])
            for elem in r.json()]
