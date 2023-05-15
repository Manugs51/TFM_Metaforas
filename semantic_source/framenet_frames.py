from typing import List, Tuple
from my_requests import my_request_get
from semantic_source.abstract_semantic_source import SemanticSource # pylint: disable=import-error
from links.babel_html_api import api # pylint: disable=import-error
import requests
from nltk.corpus import framenet as fn
import nltk



class FramenetFrames(SemanticSource):
    def __init__(self, key: str):
        nltk.download('framenet_v17')
        key_part = '?key=' + key
        incomplete_synset_part = '&id='
        search_spanish = '&' + api['search_spanish']
        incomplete_getIds_part = '&lemma='
        self.complete_url = api['information_given_synset_url'] + key_part + '&targetLang=EN' + incomplete_synset_part
        self.complete_getIds_url = api['synsets_given_word_url'] + key_part + search_spanish + incomplete_getIds_part

    def find_metaphors(self, words: List[Tuple[str, str]]):
        suj_word, suj_id = self.subject(words)
        atr_word, atr_id = self.attribute(words)

        info_of_suj = my_request_get(self.complete_url+suj_id).json()
        info_of_atr = my_request_get(self.complete_url+atr_id).json()
        print(self.complete_url+suj_id)
        print(info_of_suj)
        print('-------------------')

        #print(info_of_suj)
        #print(info_of_atr)
        senses_of_suj = []
        try:
            print("try suj")
            senses_of_suj = [info_of_suj['senses']]
        except Exception as _:
            print("catch suj")
            correct_ids_of_suj = my_request_get(self.complete_getIds_url+suj_word).json()
            for correct_id in correct_ids_of_suj:
                response = my_request_get(self.complete_url + correct_id["id"]).json()
                senses = response['senses']
                senses_of_suj.append(senses)
        senses_of_suj = [item for sublist in senses_of_suj for item in sublist]
        
        senses_of_atr = []
        try:
            print("try atr")
            senses_of_atr = [info_of_atr['senses']]
        except Exception as _:
            print("catch atr")
            correct_ids_of_atr = my_request_get(self.complete_getIds_url+atr_word).json()
            senses_of_atr = [my_request_get(self.complete_url+correct_id["id"]).json()['senses'] for correct_id in correct_ids_of_atr]
        senses_of_atr = [item for sublist in senses_of_atr for item in sublist]

        sense_names_of_suj = set(map(lambda elem : elem['properties']["simpleLemma"], senses_of_suj))
        sense_names_of_atr = set(map(lambda elem : elem['properties']["simpleLemma"], senses_of_atr))

        print(sense_names_of_suj)
        print(sense_names_of_atr)

        frames_of_suj = [fn.frames_by_lemma(sense_name) for sense_name in sense_names_of_suj]
        frames_of_atr = [fn.frames_by_lemma(sense_name) for sense_name in sense_names_of_atr]

        frame_id_set_of_suj = set(map(lambda elem : str(elem.ID), [item for sublist in frames_of_suj for item in sublist]))
        frame_id_set_of_atr = set(map(lambda elem : str(elem.ID), [item for sublist in frames_of_atr for item in sublist]))

        print(frame_id_set_of_suj)
        print(frame_id_set_of_atr)
        ret = {
            'isMetaphor': True,
            'relation': [],
        }
        print("check is metaphor")
        for c in frame_id_set_of_suj:
            if c in frame_id_set_of_atr:
                ret['isMetaphor'] = False
                ret['relation'].append(c)
        
        if ret['isMetaphor']:
            ret['reason'] = suj_word + ' y ' + atr_word + ' no tienen ningun frame en común: ' + \
                str([lambda x: fn.frame(x), frame_id_set_of_suj]) + ' y ' + str([lambda x: fn.frame(x), frame_id_set_of_atr]) 
        else:
            ret['reason'] = suj_word + ' y ' + atr_word + ' comparten los frames de:'
            for c in ret['relation']:
                ret['reason'] += ' ' + c + ','
            ret['reason'] = ret['reason'][:-1]
        return ret

    def toString(self) -> str:
        return 'babel_categories'