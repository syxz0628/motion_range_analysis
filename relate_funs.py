import os
import sys


def max_index(lst_int):
    index = []
    max_n = max(lst_int)
    for i in range(len(lst_int)):
        if lst_int[i] == max_n:
            index.append(i)
    return index  # 返回一个列表


def writelog(path2log, writeinfo):
    if path2log != None:
        print('<log> --> ', writeinfo)
        with open(path2log, 'a+') as logfile:
            logfile.writelines(writeinfo + os.linesep)


def fun_trend(newX, X1, X2, Y1, Y2):
    newY = 0
    #    newY=Y1+(Y2-Y1)*(newX-X1)/(X2-X1)
    print('newY=', newY)
    return newY