import poloniex
import pandas as pd
import sys
from time import time
from api_conf import *

def getCharts(pair):
    api = poloniex.Poloniex(key,secret,jsonNums=float)


    raw = api.returnChartData(pair, period=api.DAY, start=time()-api.YEAR*10)
    #print(raw)
    df = pd.DataFrame(raw)

# adjust dates format and set dates as index
    df['date'] = pd.to_datetime(df["date"], unit='s')
    df.set_index('date', inplace=True)

# show the end of dataframe
    print(df.tail())

try:
    if sys.argv[0] != '':
        pair = str(sys.argv[1])
        print("Getting %s" % pair)
        ret = getCharts(pair)
        print(ret)
except:
    pair = 'BTC_ETH'
    print("Getting %s" % pair)
    ret = getCharts(pair)
    print(ret)
