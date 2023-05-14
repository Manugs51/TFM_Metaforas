from typing import List, Tuple
from my_requests import my_request_get
from semantic_source.abstract_semantic_source import SemanticSource # pylint: disable=import-error
from links.babel_html_api import api # pylint: disable=import-error
import requests


class BabelCategories(SemanticSource):
    def __init__(self, key: str):
        key_part = '?key=' + key
        incomplete_synset_part = '&id='
        search_spanish = '&' + api['search_spanish']
        incomplete_getIds_part = '&lemma='
        self.complete_url = api['information_given_synset_url'] + key_part + incomplete_synset_part
        self.complete_getIds_url = api['synsets_given_word_url'] + key_part + search_spanish + incomplete_getIds_part

    def find_metaphors(self, words: List[Tuple[str, str]]):
        suj_word, suj_id = self.subject(words)
        atr_word, atr_id = self.attribute(words)

        info_of_suj = my_request_get(self.complete_url+suj_id).json()
        info_of_atr = my_request_get(self.complete_url+atr_id).json()

        #print(info_of_suj)
        #print(info_of_atr)
        categories_of_suj = []
        try:
            print("try suj")
            categories_of_suj = [info_of_suj['categories']]
        except Exception as _:
            print("catch suj")
            correct_ids_of_suj = my_request_get(self.complete_getIds_url+suj_word).json()
            print(correct_ids_of_suj)
            for correct_id in correct_ids_of_suj:
                print(self.complete_url + correct_id["id"])
                response = my_request_get(self.complete_url + correct_id["id"]).json()
                categories = response['categories']
                categories_of_suj.append(categories)
        categories_of_suj = [item for sublist in categories_of_suj for item in sublist]
        
        categories_of_atr = []
        try:
            print("try atr")
            categories_of_atr = [info_of_atr['categories']]
        except Exception as _:
            print("catch atr")
            correct_ids_of_atr = my_request_get(self.complete_getIds_url+atr_word).json()
            categories_of_atr = [my_request_get(self.complete_url+correct_id["id"]).json()['categories'] for correct_id in correct_ids_of_atr]
        categories_of_atr = [item for sublist in categories_of_atr for item in sublist]

        category_names_of_suj = set(map(lambda elem : elem['category'], categories_of_suj))
        category_names_of_atr = set(map(lambda elem : elem['category'], categories_of_atr))
        #print(category_names_of_suj)
        #print(category_names_of_atr)
        ret = {
            'isMetaphor': True,
            'relation': [],
        }
        print("check is metaphor")
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