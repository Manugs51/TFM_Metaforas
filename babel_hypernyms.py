from semantic_source import SemanticSource
from babel_html_api import api
import requests


class BabelHypernyms(SemanticSource):
    def __init__(self, key: str):
        key_part = '?key=' + key
        incomplete_synset_part = '&id='
        self.complete_url = api['edges_given_synset_url'] + key_part + incomplete_synset_part
    
    def x_in_hyps_of_y(self, x:str, y:str, already_checked:set) -> str:
        edges_of_y = requests.get(self.complete_url+y).json()

        hyps_of_y = list(filter(lambda elem : elem['pointer']['relationGroup'] == 'HYPERNYM', edges_of_y))

        ids_of_hyps_of_y = set(map(lambda edge : edge['target'], hyps_of_y))

        print('COMPROBANDO ID: ', y)
        print(ids_of_hyps_of_y)

        ret = 'hay metáfora'

        if x in ids_of_hyps_of_y: # perro es animal
            ret = 'no hay metáfora'
        else:
            for id_of_hyp_of_y in ids_of_hyps_of_y:
                if not id_of_hyp_of_y in already_checked:
                    already_checked.add(id_of_hyp_of_y)
                    if self.x_in_hyps_of_y(x, id_of_hyp_of_y, already_checked) == 'no hay metáfora': # perro es ser vivo (perro -> animal -> ser vivo)
                        ret = 'no hay metáfora'
        
        return ret



    def find_metaphors(self, words: [(str, str)]) -> str:
        suj_word, suj_id = self.subject(words)
        atr_word, atr_id = self.attribute(words)
        already_checked = set() #TODO también hace falta ponerle una profundidad máxima

        if suj_id == atr_id: #TODO refactor de return
            return 'no hay metafora'
        
        ret = self.x_in_hyps_of_y(suj_id, atr_id, already_checked)
        print('COMPROBANDO A LA INVERSA')
        if ret == 'hay metáfora':
            ret = self.x_in_hyps_of_y(atr_id, suj_id, already_checked)
        
        return ret

    def toString(self) -> str:
        return 'babel_hypernyms'
