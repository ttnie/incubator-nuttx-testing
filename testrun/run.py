#!/usr/bin/python3

import os, sys, time
from common import *
import argparse


def main():
    arg = argparse.ArgumentParser()
    arg.add_argument("-b", dest='board', default='sim',
                    help="specify board value, for example: sim or amebaZ, default is sim")
    arg.add_argument('-l', dest='log', default='.',
                    help="specify log path")
    arg.add_argument('-p', dest='path', default='.',
                    help="specify source code dir")
    args = arg.parse_args()

    board = args.board
    log = args.log
    path = args.path

    #check the argument
    if not os.path.exists(path):
        print("please set source code path!")
        sys.exit()

    if not os.path.exists(log):
        os.makedirs(log)

    #get case list from buildin_list.h and write to open_posix_list_20200921.txt
    readBuildInList(path, log)

    today = time.strftime("%Y%m%d", time.localtime())
    #get test suite list from log path
    tsList = findFile(log, '_list_%s.txt' % today)

    dic = {}
    for tsFile in tsList:
        #get Summary for test suite
        #get test suite name from test suite list file
        #for example: open_posix_list_20200921.txt, test suite: open_posix
        ts = getTsName(tsFile)

        #get case list from ts file
        f = open(tsFile, 'r')
        cList = f.readlines()
        f.close()

        #run test case
        for case in cList:
            case = case.strip("\n")
            p = connectNuttx()
            p.setup(path, os.path.join(log, case + ".txt"))
            ret = p.sendCommand(case)

            #get PASS FAIL result
            dic = getResult(case, ret, dic)

            p.cleanup()

        #follow the dailyRunList generate new dic
        tmpDic = updateDic(dic)

        #write result to csv
        writeCsv(tmpDic, log, ts)


if __name__ == '__main__':
    main()
