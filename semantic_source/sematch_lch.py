from typing import List, Tuple
from semantic_source.abstract_semantic_source import SemanticSource # pylint: disable=import-error
from links.babel_html_api import api # pylint: disable=import-error
from sematch.semantic.similarity import WordNetSimilarity


class SematchLch(SemanticSource):
    def __init__(self):
        self.wns = WordNetSimilarity()

    def find_metaphors(self, words: List[Tuple[str, str]]):
        suj_word, suj_id = self.subject(words)
        atr_word, atr_id = self.attribute(words)
        
        ret = {
            'isMetaphor': True,
            'relation': [],
        }

        relation = self.wns.monol_word_similarity(suj_word, atr_word, 'spa', 'lch')

        if relation > 0.5:
            ret['isMetaphor'] = False
        
        ret['relation'].append(relation)
        
        if ret['isMetaphor']:
            ret['reason'] = suj_word + ' y ' + atr_word + ' no están lo suficientemente relacionadas: ' + str(relation)
        else:
            ret['reason'] = suj_word + ' y ' + atr_word + ' están muy relacionadas:' + str(relation)

        return ret

    def toString(self) -> str:
        return 'sematch_lch'
