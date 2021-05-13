import flask
from flask import request, jsonify
from secrets import secrets
from babel_categories import BabelCategories
from babel_hypernyms import BabelHypernyms
from babel_lemmas_of_senses import BabelLemmasOfSenses
from babel_parser import BabelParser

app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/', methods=['GET'])
def home():
    return "<h1>API para reconocimiento de metáforas</h1><p>Esta es un prototipo de API para reconocimiento de metáforas en castellano.</p>"

def parse_mode(args, key):
    if not 'parser' in args: # Default
        return BabelParser(key)
    elif args['parser'] == 'babel_parser':
        return BabelParser(key)
    else:
        raise Exception('El parser elegido no existe')

def source_mode(args, key):
    if not 'mode' in args:
        raise Exception('No se ha elegido un método de comprobación')
    elif args['mode'] == 'babel_categories':
        return BabelCategories(key)
    elif args['mode'] == 'babel_hypernyms':
        return BabelHypernyms(key)
    elif args['mode'] == 'babel_senses':
        return BabelLemmasOfSenses(key)
    else:
        raise Exception('El método de comprobación elegido no existe')

def choose_parser_key(args):
    if 'parser_key' in args:
        return args['parser_key']
    else:
        return secrets['babel_key']

def choose_source_key(args):
    if 'mode_key' in args:
        return args['mode_key']
    else:
        return secrets['babel_key']

def get_text(args):
    if 'text' in args:
        return args['text']
    else:
        raise Exception('Es necesario proporcionar el texto a analizar')

@app.route('/api/v1/check', methods=['GET'])
def api_v1_check():

    #TODO comprobar si la API de babel no devuelve nada

    parser_key = choose_parser_key(request.args)

    source_key = choose_source_key(request.args)

    parser = parse_mode(request.args, parser_key)

    source = source_mode(request.args, source_key)

    text = get_text(request.args)

    word_and_id = None 
    try:
        word_and_id = parser.parse(text)
    except:
        raise Exception('Hubo un problema analizando sintácticamente el texto')
    
    metaphors_found = None
    try:
        metaphors_found = source.find_metaphors(word_and_id)
    except:
        raise Exception('Hubo un problema buscando la metáfora')

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
