import pandas as pd
from statistics import mean, mode
import app
import sys

if __name__ == '__main__':
    df = pd.read_excel('dataset_original.xlsx')
    socore = {
        '-1': 0,
        '0': 0,
        '1': 0,
        '2': 0,
        '3': 0,
    }
    aux = {}
    puntuaciones = []
    for m in df['Score']:
        if type(m) is int:
            if m < 0:
                aux[-1] = aux.get(-1,0) + 1
                puntuaciones.append(-1)
            else:
                aux[m] = aux.get(m,0) + 1
                puntuaciones.append(m)
        elif type(m) is str:
            ms = m.split(', ')
            if m == 'VACIO':
                aux['VACIO'] = aux.get('VACIO', 0) + 1
                puntuaciones.append('VACIO')
            elif mode(ms) == '-1':
                aux[-1] = aux.get(-1, 0) + 1
                puntuaciones.append(-1)
            elif mode(ms) == 'VACIO':
                aux['VACIO'] = aux.get('VACIO', 0) + 1
                puntuaciones.append('VACIO')
            else:
                for idx, msp in enumerate(ms):
                    if msp == '-1' or msp == 'VACIO':
                        ms[idx] = 0
                    ms[idx] = int(ms[idx])
                avg=mean(ms)
                aux[avg] = aux.get(avg, 0) + 1
                puntuaciones.append(avg)
        else:
            print(type(m))
            aux['error'+str(m)] = aux.get('error'+str(m),0) + 1
            puntuaciones.append('error'+str(m))
    
    df_res = pd.DataFrame(puntuaciones)
    df_res.to_excel('dataset_scores_correctos.xlsx')
    print(aux)