from typing import List, Tuple
from links.babel_html_api import api # pylint: disable=import-error
import requests
from custom_parser.abstract_parser import Parser # pylint: disable=import-error
import spacy

class SpacyParser(Parser):
    def __init__(self, key: str):
        self.nlp = spacy.load("es_core_news_lg")
    
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
        return [
                (doc_subj.text, doc_subj.dep_),
                ('','cop'),
                (doc_atrb.text, doc_atrb.dep_)
                ]
    
    def toString(self) -> str:
        return 'babel_parser'
