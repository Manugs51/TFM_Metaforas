from semantic_source import SemanticSource
from babel_html_api import api
import requests


class BabelLemmasOfSenses(SemanticSource):
    def __init__(self, key: str):
        key_part = '?key=' + key
        lang_part = '&' + api['search_spanish']
        incomplete_lemma_part = '&lemma='
        self.complete_url = api['senses_given_word_url'] + key_part + lang_part + incomplete_lemma_part

    def find_metaphors(self, words: [(str, str)]) -> str:
        suj_word, suj_id = self.subject(words)
        atr_word, atr_id = self.attribute(words)

        senses_of_suj = requests.get(self.complete_url+suj_word).json()
        senses_of_atr = requests.get(self.complete_url+atr_word).json()

        #list of lists of jsons
        #synsets_of_words_response = [requests.get(self.complete_url+w[0]).json() for w in words]
        
        lemmas_of_senses_of_suj = set(map(lambda elem : elem['properties']['simpleLemma'], senses_of_suj)) 
        lemmas_of_senses_of_atr = set(map(lambda elem : elem['properties']['simpleLemma'], senses_of_atr)) 
        #list of lists of ids
        #print([list(map(lambda elem : elem['properties']['simpleLemma'], s)) for s in synsets_of_words_response])
        #synsets_of_words = [list(map(lambda elem : elem['properties']['simpleLemma'], s)) 
        #                    for s in synsets_of_words_response]
        #TODO refactor
        #noun1 = sorted(synsets_of_words[0])
        #print(noun1)
        #noun2 = sorted(synsets_of_words[2])
        #print(noun2)
        print(lemmas_of_senses_of_suj)
        print(lemmas_of_senses_of_atr)
        
        ret = {
            'isMetaphor': True,
            'relation': [],
        }

        for lemma in lemmas_of_senses_of_suj:
            if lemma in lemmas_of_senses_of_atr:
                ret['isMetaphor'] = False
                ret['relation'].append(lemma)
        
        if ret['isMetaphor']:
            ret['reason'] = suj_word + ' y ' + atr_word + ' no tienen ningún sentido común: ' + \
                str(lemmas_of_senses_of_suj) + ' y ' + str(lemmas_of_senses_of_atr)
        else:
            ret['reason'] = suj_word + ' y ' + atr_word + ' comparten los sentidos:'
            for c in ret['relation']:
                ret['reason'] += ' ' + c + ','
            ret['reason'] = ret['reason'][:-1]

        return ret

    def toString(self) -> str:
        return 'babel_senses'
