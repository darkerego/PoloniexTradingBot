#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys,json
ret = ''
data = ''
import poloniex
import api_conf

def gen():
    key = str(api_conf.key)
    secret = str(api_conf.secret)
    data = poloniex.Poloniex(key,secret)
    try:
        x = data.returnAvailableAccountBalances()
    except:
        pass
    else:
        k = dict.keys(x)
        for i in k:
            i = str(i)
            print(x[i])
            #print("\n")
        return(x)
        
   


def parse():
    ret = gen()
    xx = json.dumps(ret)
    return xx
   # xxx = json.dumps([xx], separators=(',', ':'))
   # print(str(xxx))

_ret = parse()
#print(_ret)
#k = dict.keys(_ret)
#for i in k:
#    print([i])
