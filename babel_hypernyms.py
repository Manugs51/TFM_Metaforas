from semantic_source import SemanticSource
from babel_html_api import api
import requests


class BabelHypernyms(SemanticSource):
    def __init__(self, key: str):
        key_part = '?key=' + key
        incomplete_synset_part = '&id='
        self.complete_url = api['edges_given_synset_url'] + key_part + incomplete_synset_part
    
    def x_in_hyps_of_y(self, x:str, y:str, depth:int) -> str:
        edges_of_y = requests.get(self.complete_url+y).json()

        hyps_of_y = list(filter(lambda elem : elem['pointer']['relationGroup'] == 'HYPERNYM', edges_of_y))

        ids_of_hyps_of_y = set(map(lambda edge : edge['target'], hyps_of_y))

        print('COMPROBANDO ID: ', y)
        print(ids_of_hyps_of_y)

        ret = {
            'isMetaphor': True,
            'relation': [],
        }

        if x in ids_of_hyps_of_y: # perro es animal
            ret['isMetaphor'] = False
            ret['relation'].append(x)
        else:
            for id_of_hyp_of_y in ids_of_hyps_of_y:
                if depth < 4:
                    #already_checked.add(id_of_hyp_of_y)
                    ret_hyps = self.x_in_hyps_of_y(x, id_of_hyp_of_y, depth+1) # perro es ser vivo (perro -> animal -> ser vivo)
                    if not ret_hyps['isMetaphor']:
                        ret['relation'] = ret_hyps['relation']
                        ret['relation'].append(id_of_hyp_of_y)
                        ret['isMetaphor'] = False
                        break
        
        return ret



    def find_metaphors(self, words: [(str, str)]) -> str:
        suj_word, suj_id = self.subject(words)
        atr_word, atr_id = self.attribute(words)
        already_checked = set() #TODO combinar con depth

        if suj_id == atr_id:
            return {
                'isMetaphor': False,
                'relation': [suj_id],
                'reason': 'Tanto el sujeto como el atributo de la oración son la misma palabra'
            }
        
        ret = self.x_in_hyps_of_y(suj_id, atr_id, 0)
        print('COMPROBANDO A LA INVERSA')
        if ret['isMetaphor']:
            ret = self.x_in_hyps_of_y(atr_id, suj_id, 0)
            if not ret['isMetaphor']:
                ret['relation'].append(suj_id)
        else:
            ret['relation'].append(atr_id)

        if ret['isMetaphor']:
            ret['reason'] = 'Sujeto (' + suj_id + ') y atributo (' + atr_id + ') no tienen relación de hiperonimia'
        else:
            ret['reason'] = 'Existe una relación de hiperonimia'
            for id in reversed(ret['relation']):
                ret['reason'] += ' -> ' + id
        
        return ret

    def toString(self) -> str:
        return 'babel_hypernyms'
