import pandas as pd
import app
import sys

if __name__ == '__main__':
    df = pd.read_excel('dataset.xlsx')
    print(df)
    print(len(df))
    args={
        'parser_key': '420b7865-2698-4899-b95e-b8b5f20f8d8d',
        'mode_key': '420b7865-2698-4899-b95e-b8b5f20f8d8d',
        'parser': 'spacy_parser',
        'mode': 'sematch_wup',
    }

    try:
        parser_key = app.choose_parser_key(args)

        source_key = app.choose_source_key(args)

        parser = app.parse_mode(args, parser_key)

        source = app.source_mode(args, source_key)
    except Exception as e:
        print(e)
        exit()
    result = []
    count=0
    for m in df['Metáfora']:
        args['text'] = m

        text = app.get_text(args)

        word_and_id = None
        try:
            word_and_id = parser.parse(text)
        except Exception as _:
            print('Hubo un problema analizando sintácticamente el texto')
            print(text)
            result.append([text, parser.toString(), source.toString(),'---', '---', '---'])
            count += 1
            continue

        metaphors_found = None
        try:
            metaphors_found = source.find_metaphors(word_and_id)
        except Exception as _:
            print('Hubo un problema buscando la metáfora')
            print(text)
            result.append([text, parser.toString(), source.toString(),'---', '---', '---'])
            count += 1
            continue
        result.append([text, parser.toString(), source.toString(), metaphors_found['isMetaphor'], metaphors_found['reason'], str(metaphors_found['relation'])])

        results_filename = 'results0.xlsx'
        if count % 10 == 0:
            if count % 100 == 0:
                results_filename = 'results' + str(count) + '.xlsx'
            print(count)
            df_res = pd.DataFrame(result)
            df_res.to_excel(results_filename)
        count += 1
    df_res = pd.DataFrame(result)
    df_res.to_excel('results_tot_wup.xlsx')
    '''
    print({
        'text': text,
        'parser': parser.toString(),
        'mode': source.toString(),
        'relation': metaphors_found['relation'],
        'isMetaphor': metaphors_found['isMetaphor'],
        'reason': metaphors_found['reason'],
    })
    '''