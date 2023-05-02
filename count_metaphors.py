import pandas as pd
import math
from statistics import mean, mode
import app
import sys

if __name__ == '__main__':
    df = pd.read_excel('dataset_original.xlsx')
    aux = {}
    for m in df['Score_num']:
        if type(m) is str:
            aux[m] = aux.get(m, 0) + 1
        else:
            score = math.ceil(m)
            aux[score] = aux.get(score,0) + 1
    print(aux)
    # {0: 391, -1: 139, 1: 145, 2: 279, 3: 126, 'VACIO': 551}