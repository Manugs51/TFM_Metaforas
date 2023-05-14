"""App base module"""

from custom_parser.spacy_babel_parser import SpacyBabelParser
from private_secrets import secrets
from flask import request
import flask
from custom_parser.babel_parser import BabelParser
from custom_parser.abstract_parser import Parser
from custom_parser.spacy_parser import SpacyParser
from semantic_source.abstract_semantic_source import SemanticSource
from semantic_source.babel_categories import BabelCategories
from semantic_source.babel_hypernyms import BabelHypernyms
from semantic_source.babel_lemmas_of_senses import BabelLemmasOfSenses
from semantic_source.sematch_jcn import SematchJcn
from semantic_source.sematch_lch import SematchLch
from semantic_source.sematch_li import SematchLi
from semantic_source.sematch_lin import SematchLin
from semantic_source.sematch_path import SematchPath
from semantic_source.sematch_res import SematchRes
from semantic_source.sematch_wpath import SematchWpath
from semantic_source.sematch_wup import SematchWup


app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/', methods=['GET'])
def home() -> str:
    """ View of the API """

    return "<h1>API para reconocimiento de metáforas</h1><p>Esta es un prototipo de API para\
         reconocimiento de metáforas en castellano.</p>"

def parse_mode(args, key) -> Parser:
    """ Returns the object that will parse the sentence to obtain the tokens """

    if not 'parser' in args: # Default
        return BabelParser(key)
    elif args['parser'] == 'babel_parser':
        return BabelParser(key)
    elif args['parser'] == 'spacy_parser':
        return SpacyParser(key)
    elif args['parser'] == 'spacy_babel_parser':
        return SpacyBabelParser(key)

    raise Exception('El parser elegido no existe')

def source_mode(args, key) -> SemanticSource:
    """ Returns the object that will check if there is a metaphore """

    if not 'mode' in args:
        raise Exception('No se ha elegido un método de comprobación')
    elif args['mode'] == 'babel_categories':
        return BabelCategories(key)
    elif args['mode'] == 'babel_hypernyms':
        return BabelHypernyms(key)
    elif args['mode'] == 'babel_senses':
        return BabelLemmasOfSenses(key)
    elif args['mode'] == 'sematch_jcn':
        return SematchJcn()
    elif args['mode'] == 'sematch_lch':
        return SematchLch()
    elif args['mode'] == 'sematch_li':
        return SematchLi()
    elif args['mode'] == 'sematch_lin':
        return SematchLin()
    elif args['mode'] == 'sematch_path':
        return SematchPath()
    elif args['mode'] == 'sematch_res':
        return SematchRes()
    elif args['mode'] == 'sematch_wpath':
        return SematchWpath()
    elif args['mode'] == 'sematch_wup':
        return SematchWup()

    raise Exception('El método de comprobación elegido no existe')

def choose_parser_key(args) -> str:
    """
        Returns the key given by the user for the parse system
        if no key is given, returns a default key
    """

    if 'parser_key' in args:
        return args['parser_key']

    return secrets['babel_key']

def choose_source_key(args):
    """
        Returns the key given by the user for the semantic source system
        if no key is given, returns a default key
    """

    if 'mode_key' in args:
        return args['mode_key']

    return secrets['babel_key']

def get_text(args):
    """ Returns the text to analyze """

    if 'text' in args:
        return args['text']

    raise Exception('Es necesario proporcionar el texto a analizar')

@app.route('/api/v1/check', methods=['GET'])
def api_v1_check():
    """
        V1, checks whether a text contains a metaphor
    """

    try:
        parser_key = choose_parser_key(request.args)

        source_key = choose_source_key(request.args)

        parser = parse_mode(request.args, parser_key)

        source = source_mode(request.args, source_key)

        text = get_text(request.args)
    except Exception as e:
        return e, 500

    word_and_id = None
    try:
        word_and_id = parser.parse(text)
    except Exception as _:
        return 'Hubo un problema analizando sintácticamente el texto', 500

    metaphors_found = None
    try:
        metaphors_found = source.find_metaphors(word_and_id)
    except Exception as _:
        return 'Hubo un problema buscando la metáfora', 500

    return {
        'text': text,
        'parser': parser.toString(),
        'mode': source.toString(),
        'relation': metaphors_found['relation'],
        'isMetaphor': metaphors_found['isMetaphor'],
        'reason': metaphors_found['reason'],
    }, 200, {'Access-Control-Allow-Origin': '*'}

if __name__ == '__main__':
    app.run()
