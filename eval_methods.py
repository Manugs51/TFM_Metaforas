import statistics
import pandas as pd
import math
from statistics import mean, mode
import app
import sys

if __name__ == '__main__':
    df = pd.read_excel('dataset_comparacion.xlsx')
    scoreVACIO = []
    evalsVACIO = []
    score0 = []
    evals0 = []
    score_1 = []
    evals_1 = []
    score1 = []
    evals1 = []
    score2 = []
    evals2 = []
    score3 = []
    evals3 = []
    scoreSI = []
    evalsSI = []
    scoreNO = []
    evalsNO = []
    for idx, row in df.iterrows():
        score = row['Score_num']
        evals = eval(row['Relacion_spacy_wup'])[0] # CAMBIAR por método evaluado
        if score == 'VACIO':
            scoreVACIO.append(score)
            evalsVACIO.append(evals)
        elif score == -1:
            score_1.append(score)
            evals_1.append(evals)
        elif score == 0:
            score0.append(score)
            evals0.append(evals)
            scoreNO.append(score)
            evalsNO.append(evals)
        elif score <= 1 and score > 0:
            score1.append(score)
            evals1.append(evals)
            scoreSI.append(score)
            evalsSI.append(evals)
        elif score > 1 and score <= 2:
            score2.append(score)
            evals2.append(evals)
            scoreSI.append(score)
            evalsSI.append(evals)
        elif score > 2 and score <= 3:
            score3.append(score)
            evals3.append(evals)
            scoreSI.append(score)
            evalsSI.append(evals)
    print(evalsSI)
    print(evalsNO)
    print(statistics.median(evalsSI))
    # jcn: 0
    # lch: 0
    # li: 0
    # lin: 0
    # path: 0
    # res: 0
    # wpath: 0
    # wup: 0
    print(statistics.median(evalsNO))
    # jcn: 0
    # lch: 0
    # li: 0
    # lin: 0
    # path: 0
    # res: 0
    # wpath: 0
    # wup: 0
    print(statistics.mean(evalsSI))
    # jcn: 0.03544622077327623
    # lch: 0.5933808383438078
    # li: 0.08347571546820087
    # lin: 0.09127213634202042
    # path: 0.05697052947052947
    # res: 0.8728737980083032
    # wpath: 0.08617002964130233
    # wup: 0.17089234738742198
    print(statistics.mean(evalsNO))
    # jcn: 0.05421532491387382
    # lch: 0.5492304101445705
    # li: 0.10034105211366132
    # lin: 0.10739993340408961
    # path: 0.07149487341303198
    # res: 5.115089514066496e+297
    # wpath: 0.09873840081466634
    # wup: 0.16357447219529836
    print('--')
    print(statistics.median(evalsVACIO))
    print(statistics.median(evals_1))
    print(statistics.median(evals1))
    print(statistics.median(evals2))
    print(statistics.median(evals3))
    # jcn
    #    0
    #    0
    #    0
    #    0
    #    0.0
    # lch
    #    0
    #    0
    #    0
    #    0
    #    0.0
    # li
    #    0
    #    0
    #    0
    #    0
    #    0.0
    # lin
    #    0
    #    0
    #    0
    #    0
    #    0.0
    # path
    #    0
    #    0
    #    0
    #    0
    #    0.0
    # res
    #    0
    #    0
    #    0
    #    0
    #    0.0
    # wpath
    #    0
    #    0
    #    0
    #    0
    #    0.0
    # wup
    #    0
    #    0
    #    0
    #    0
    #    0.0
    print(statistics.mean(evalsVACIO))
    print(statistics.mean(evals_1))
    print(statistics.mean(evals1))
    print(statistics.mean(evals2))
    print(statistics.mean(evals3))
    # jcn
    #    0.041700708277458316
    #    0.029584691748450877
    #    0.04692821645101064
    #    0.034156440684622216
    #    0.025088754673776085
    # lch
    #    0.5196956389232282
    #    0.36642933753197166
    #    0.6089387542575634
    #    0.6170758720405366
    #    0.5230093128764914
    # li
    #    0.07886829284681017
    #    0.05398745495724461
    #    0.09855516174449323
    #    0.09117701289750962
    #    0.04906951155677599
    # lin
    #    0.08226849332229078
    #    0.05466701112504239
    #    0.10582653014196558
    #    0.10020427785002714
    #    0.05474471902673528
    # lin
    #    0.058506008006915446
    #    0.04105230594862419
    #    0.06756232273473653
    #    0.058378648432411875
    #    0.04166358333025
    # res
    #    0.8367222433031973
    #    0.5858893652459956
    #    1.0071971244813807
    #    0.9712649740176911
    #    0.5004291913002443
    # wpath
    #    0.07848372533114731
    #    0.05449423512915233
    #    0.09408530434499349
    #    0.0951410395830555
    #    0.05719680261126777
    # wup
    #    0.14905756379013557
    #    0.10424786561388116
    #    0.1816499524815955
    #    0.18187231979219062
    #    0.13419976770817107
