!/usr/bin/python3
import sys
ret = ''
import poloniex
import api_conf

def gen():
    key = str(api_conf.key)
    secret = str(api_conf.secret)
    data = poloniex.Poloniex(key,secret)
    try:
        ret = data.returnCompleteBalances()
        x = data.returnTradeHistory()
    except:
        pass
    else:
        for i in x:
            print("\n")
            print(x[i])
            

   
        return ret



ret = gen()
