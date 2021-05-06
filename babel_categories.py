from semantic_source import SemanticSource
from babel_html_api import api
import requests


class BabelCategories(SemanticSource):
    def __init__(self, key: str):
        key_part = '?key=' + key
        incomplete_synset_part = '&id='
        self.complete_url = api['information_given_synset_url'] + key_part + incomplete_synset_part

    def find_metaphors(self, words: [(str, str)]):
        suj_word, suj_id = self.subject(words)
        atr_word, atr_id = self.attribute(words)

        info_of_suj = requests.get(self.complete_url+suj_id).json()
        info_of_atr = requests.get(self.complete_url+atr_id).json()
        
        categories_of_suj = info_of_suj['categories']
        categories_of_atr = info_of_atr['categories']
        
        category_names_of_suj = set(map(lambda elem : elem['category'], categories_of_suj))
        category_names_of_atr = set(map(lambda elem : elem['category'], categories_of_atr))
        
        print(category_names_of_suj)
        print(category_names_of_atr)
        ret = {
            'isMetaphor': True,
            'relation': [],
        }
        for c in category_names_of_suj:
            if c in category_names_of_atr:
                ret['isMetaphor'] = False
                ret['relation'].append(c)
        
        if ret['isMetaphor']:
            ret['reason'] = suj_word + ' y ' + atr_word + ' no tienen ninguna categoría en común: ' + \
                str(category_names_of_suj) + ' y ' + str(category_names_of_atr)
        else:
            ret['reason'] = suj_word + ' y ' + atr_word + ' comparten las categorías de:'
            for c in ret['relation']:
                ret['reason'] += ' ' + c + ','
            ret['reason'] = ret['reason'][:-1]
        return ret

    def toString(self) -> str:
        return 'babel_categories'