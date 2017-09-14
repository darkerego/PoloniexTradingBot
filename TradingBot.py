#!/usr/bin/python2
# -*- coding: utf-8 -*-
import datetime
import time
import argparse
import sys
try:
    # For Python 3+
    from configparser import ConfigParser, NoSectionError
except ImportError:
    # Fallback to Python 2.7
    from ConfigParser import ConfigParser, NoSectionError
# get the real api from here: https://github.com/darkerego/python-poloniex, the included one sucks
import poloniex
def createTimeStamp(datestr, format="%Y-%m-%d %H:%M:%S"):
    return time.mktime(time.strptime(datestr, format))
def sum(array):
    ret = float(0.0)
    for x in array:
        x = float(x)
        #ret = float(ret)
        ret += x
    return ret

def percentage(part, whole):
  return 100 * float(part)/float(whole)




def main(argv):
    parser = argparse.ArgumentParser(description='Poloniex Trading Bot')
    parser.add_argument('-p', '--pair', default='BTC_ETH', type=str, required=False, help='Coin pair to trade between [default: BTC_ETH]')
    parser.add_argument('-i', '--interval', default=1, type=float, required=False, help='seconds to sleep between loops [default: 1]')
    parser.add_argument('-a', '--amount', default=0.125, type=float, required=False, help='percentage of balances to buy/sell [default: 0.125]')
    parser.add_argument('-d', '--debug', default=False, action='store_true', required=False, help='enables extra console messages (for debugging)')
    parser.add_argument('-v', '--verbose', default=False, action='store_true', required=False, help='enables extra console messages (for debugging)')
    args = parser.parse_args()
    
    lastAsk = 0.0
    lastBid = 0.0
    sellTarget = 0.0
    minPrice = 0.0
    maxPrice = 0.0
    interval = args.interval
    pair = args.pair
    amt = args.amount
    amt = float(amt)
    verbose = args.verbose
    debug = args.debug

    cpair = pair.split('_')
    coin0 = cpair[0]
    coin1 = cpair[1]
    data = poloniex.Poloniex('your-api-key', 'your-secret-string')
    #demo = test()
    
    while True:
        chartClose = []
        timeNow = int(createTimeStamp('{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())))
        if timeNow % 900 != 0:
            timeNow = timeNow / 900 * 900
        try:
            lastPrice = float(data.returnTicker()[pair]['last'])
        except Exception as e:
            print("ERROR: "+e)
            break
        # period 900
        try:
            chartData = data.returnChartData(pair, 900, timeNow - 28800, timeNow)
        except Exception as e:
            print("ERROR: %s " % e)
            break
        
        
        for candle in chartData:
                try:
                        chartClose.append(candle['close'])
                        if debug: print(chartClose)
                except:
                        pass
        


        ema1 = (sum(chartClose[0:16]) / 16)
        ema1_ = ema1
        ema2 = (sum(chartClose[16:24]) / 8)
        try:
            avg = data.returnChartData(pair, 900, timeNow - 7200, timeNow)[-1]['weightedAverage']
            avg = float(avg)
        except:
            pass
        # Double exponential moving average at period 900
        try:
            DEMA = ( 2 * ema1) * (ema1 * (ema1 * 900) )
        except Exception as e:
            print(e)


        #if debug: print('EMA3 :%s' % ema3)
        for i in range(16,32):
            try:
                chartClose[i] = float(chartClose[i])
                ema1 += (chartClose[i] - ema1) * 2 / 17
            except:
                print('FATAL: cannot get charts')
                pass
        for i in range(24,32):
            try:
                ema2 += (chartClose[i] - ema2) * 2 / 9
            except:
                print('FATAL: cannot get charts')
                pass


        
        minEma = min(ema1, ema2)
        maxEMA = max(ema1,ema2)
        if debug: print("DEBUG: min average: %s" % minEma)
        buyTarget = minEma * 0.99

        
        diff = (sellTarget - buyTarget)
        orderBook = data.returnOrderBook(pair)
        lastAsk_ = orderBook['asks'][0]
        lastBid_ = orderBook['bids'][0]
        lastAsk = float(lastAsk_[0])
        lastBid = float(lastBid_[0])
        try:
            balances = data.returnAvailableAccountBalances()
        except Exception as e1:
            print('ERROR: %s' % e1)
        else:
            try:
                bal0 = balances['exchange'][coin0]
            except KeyError:
                bal0 = float(0.0)
            else:
                bal0 = float(bal0)

            try:
                bal1 = balances['exchange'][coin1]
            except KeyError:
                bal1 = float(0.0)
            else:
                bal1 = float(bal1)
        value = bal0 + (bal1 * lastBid)
        amtBuy = bal0 * amt
        amtSell = bal1 * amt



        if verbose: print('Verbose mode is on')
        print('{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now()) + ' %s :' % (pair))
        print('Last price : %.8f' %(lastPrice))
        print('Current ask : %.8f' %(lastAsk))
        print('Current bid : %.8f' %(lastBid))
        print('EMA 1 : %.8f' %ema1)
        print('EMA 2 : %.8f' %ema2)
        print('EMA min: %.8f')% minEma
        print('')
        print('EMA Average: %.8f' %avg)
        print('DEMA: %.8f' %DEMA)

        print('%s Value : %.8f' %(coin1,value))

        print('%s Balance : %.8f' % (coin0,bal0))
        print('%s Balance: %.8f' % (coin1,bal1))

        #print("Difference: %.8f" % diff)
        print("Difference: "+str(diff))
        print('Buy target : %.8f' %buyTarget)
        print('Sell target : %.8f' %sellTarget)
        print('Buy limit : %.8f' %(minPrice * 1.0025))
        print('Sell limit : %.8f' %(maxPrice * 0.995))

        
        if bal0 > 0.0005:
            if debug: print("DEBUG: Positive %s balance %s " % (coin0,bal0))
            if (lastPrice < buyTarget):
                if debug: print('DEBUG: lastPrice < buyTarget...')
                if (minPrice != 0) and(lastPrice > minPrice * 1.002):
                    print('DEBUG: minPrice is not 0')
                    #buyAt = float(lastPrice * 1.0002)
                    if (lastPrice >= buyTarget):
                        if debug: print("DEBUG: minPrice greater than 0 and lastPrice > minPrice x min")
                        amt = float(bal0)
                        
                        if verbose: print('Atemption to buy at %s ..' % buyAt)
                        if bal0 > 0.00005:
                            try:
                                data.buy(pair, lastPrice, bal0)
                            except Exception as e:
                                print("Failed to buy with error : %s" % e)
                            finally:
                                #if debug: print("Not buying...")   
                                sellTarget = lastBid * 1.02
                                minPrice = 0.0
                                maxPrice = 0.0
                                print('Buy price : %.8f' %lastPrice)
                                print('Sell target : %.8f' %sellTarget)
                else:
                        
                        if minPrice != 0:
                            minPrice = min(minPrice, lastPrice)
                        else:
                            minPrice = lastPrice
                
               
            else:
                minPrice = 0.0
        else:
            if debug: print("DEBUG: %s balance is too low to sell" % bal1)
            #sellTarget 
            if lastPrice > sellTarget:
                if debug:print("DEBUG: lastprice is greater than selltarget")
                #sellAt =
                if lastPrice < (maxPrice * 0.999):
                    if debug: print("DEBUG: lastPrice less than sell price!")
                    if bal1 >= 0.00001 or sellTarget == 0:
                        if sellTarget == 0:
                            if  maxPrice < (lastPrice * 1.0375) :
                                sellTarget = avg * 1.03
                            else:
                                sellTarget = lastPrice * 1.025

                        if verbose: print('INFO: Atemption to sell at %s ..' % sellTarget)
                        try:
                            data.sell(pair, sellTarget, bal1)
                            amt1 = float(bal)
                            print("Selling %s %s"% (amt1,coin1))
                        except Exception as lol:
                            if debug: print("DEBUG: %s" % lol)
                        print('Sell price : %.8f' %lastPrice)
                        sellTarget = 0.0
                else:
                    if verbose: print("INFO: Did not sell, lastprice was less than sell target" % (lastPrice,sellTarget))
                    maxPrice = max(maxPrice, lastPrice)
            else:
                maxPrice = 0.0
        print('***************************************************')




        time.sleep(float(interval))

if __name__ == "__main__":
    main(sys.argv[1:])
