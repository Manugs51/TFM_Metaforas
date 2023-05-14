from typing import List, Tuple
from links.babel_html_api import api # pylint: disable=import-error
import requests
from custom_parser.abstract_parser import Parser # pylint: disable=import-error
import spacy

class SpacyBabelParser(Parser):
    def __init__(self, key: str):
        self.nlp = spacy.load("es_core_news_lg")
        key_part = '?key=' + key
        lang_part = '&' + api['spanish']
        incomplete_text_part = '&text='
        self.complete_url = api['disambiguate_url'] + key_part + lang_part + incomplete_text_part
    
    def parse(self, text: str) -> List[Tuple[str, str]]:
        doc = self.nlp(text)
        try:
            doc_subj = [d for d in doc if "subj" in d.dep_][0]
        except Exception as _:
            for d in doc:
                print(d, d.dep_)
            raise Exception("No se encontró el sujeto en la frase")
        try:
            doc_atrb = [d for d in doc if "ROOT" in d.dep_][0]
        except Exception as _:
            print('b')
            raise Exception("No se encontró el atributo en la frase")
        #print(doc_subj, doc_atrb)

        while True:
            try:
                r = requests.get(self.complete_url+text, timeout=5)
                break
            except requests.Timeout:
                print("Timeout occurred, retrying...")
        #print(r.json())
        #print(doc_subj.idx, doc_subj.idx + len(doc_subj.text))
        #print(doc_atrb.idx, doc_atrb.idx + len(doc_atrb.text))
        # For synsets in json return the word (start->end) + sysnsetID
        babel_subj = ()
        babel_atrb = ()
        try:
            babel_subj = (doc_subj.text, [disambiguated_word['babelSynsetID'] for disambiguated_word in r.json() if disambiguated_word['charFragment']['start'] == doc_subj.idx and disambiguated_word['charFragment']['end'] == doc_subj.idx + len(doc_subj.text) - 1][0])
        except Exception as _:
            babel_subj = (doc_subj.text, '')
        try:
            babel_atrb = (doc_atrb.text, [disambiguated_word['babelSynsetID'] for disambiguated_word in r.json() if disambiguated_word['charFragment']['start'] == doc_atrb.idx and disambiguated_word['charFragment']['end'] == doc_atrb.idx + len(doc_atrb.text) - 1][0])
        except Exception as _:
            babel_atrb = (doc_atrb.text, '')
        return [babel_subj, ('','cop'), babel_atrb]
    
    def toString(self) -> str:
        return 'spacy_babel_parser'
