#!/usr/bin/python2
# -*- coding: utf-8 -*-

print("""
WARNING: This code is still a mess, in alpha stages. Technically it works, and makes some money,
but it's pretty untested, so use at your own risk.
""")

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
else:
    print("I hate python3! But if you insist...")
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

from termcolor import colored


def main(argv):
    parser = argparse.ArgumentParser(description='Poloniex Trading Bot')
    parser.add_argument('-p', '--pair', default='BTC_ETH', type=str, required=False, help='Coin pair to trade between [default: BTC_ETH]')
    parser.add_argument('-i', '--interval', default=5, type=float, required=False, help='seconds to sleep between loops [default: 1]')
    parser.add_argument('-b', '--amount_buy', default=0.99, type=float, required=False, help='percentage of balances to buy/sell [default: 0.99]')
    parser.add_argument('-s', '--amount_sell', default=1.02, type=float, required=False, help='percentage of balances to buy/sell [default: 1.02]')
    parser.add_argument('-v', '--verbose', default=False, action='store_true', required=False, help='enables verbose console messages')
    parser.add_argument('-m', '--mode', default='normal', type=str, required=False, help='mode: positive (smaller propfit more often) or normal')
    parser.add_argument('-d', '--debug', default=False, action='store_true', required=False, help='enables extra console messages (for debugging)')

    args = parser.parse_args()
    
    lastAsk = 0.0
    lastBid = 0.0
    sellTarget = 0.0
    minPrice = 0.0
    maxPrice = 0.0
    interval = args.interval
    pair = args.pair
    #amt = args.amount
    #amt = float(amt)
    amount_buy = args.amount_buy
    amount_sell = args.amount_sell
    amount_buy = float(amount_buy)
    amount_sell = float(amount_sell)
    mode = args.mode
    mode = str(mode)
    print("Mode: %s : " % mode)
    verbose = args.verbose
    debug = args.debug
    cpair = pair.split('_')
    coin0 = cpair[0]
    coin1 = cpair[1]
    data = poloniex.Poloniex('your-api-key', 'your-api-secret')
    #demo = test()
    
    while True:
        chartClose = []
        timeNow = int(createTimeStamp('{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())))
        if timeNow % 900 != 0:
            timeNow = timeNow / 900 * 900
        try:
            lastPrice = float(data.returnTicker()[pair]['last'])
        except Exception as e:
            print("ERROR: "+str(e))
            break
        # period 900
        try:
            chartData = data.returnChartData(pair, 900, timeNow - 28800, timeNow)
        except Exception as e:
            print("ERROR: %s " % str(e))
            break
        
        
        for candle in chartData:
                try:
                        chartClose.append(candle['close'])
                        #if debug: print(chartClose)
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
                print('FATAL: cannot get charts. Check system clock, if issue persists than generate a new api-key.')
                pass
        for i in range(24,32):
            try:
                ema2 += (chartClose[i] - ema2) * 2 / 9
            except:
                print('FATAL: cannot get charts. Check system clock, if issue persists than generate a new api-key')
                pass


        
        minEma = min(ema1, ema2)
        maxEma = max(ema1,ema2)
        if debug: print("DEBUG: min average: %s" % minEma)
        if debug: print("DEBUG: max average: %s" % maxEma)
        if debug: print("DEBUG: average: %s" % avg)
        buyTarget = minEma * amount_buy
        sellTarget = maxEma * amount_sell
        

        
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
            except KeyError as e:
                if debug: print(e)
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
        #amtBuy = bal0 * amt
        #amtSell = bal1 * amt



        if verbose: print('Verbose mode is on')
        pair_ = colored(str(pair), 'yellow')
        print('{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now()) + ' %s :' % (pair_))
        print('Last price : ')+ colored('%.8f' %(lastPrice), 'magenta',attrs=['blink'])
        print('Current ask : ')+ colored('%.8f' %(lastAsk), 'blue')
        print('Current bid : ')+ colored('%.8f' %(lastBid), 'cyan')
        print('EMA 1 : %.8f' %ema1)
        print('EMA 2 : %.8f' %ema2)
        #if debug: print('EMA min: %.8f')% minEma
        #print('- - - - - - - - - - - - - - - - - - - - - - - - - ')
        if debug: print('EMA Average: %.8f' %avg)
        #print('DEMA: %.8f' %DEMA)
        print('%s Value : %.8f' %(coin1,value))
        bal0_ = colored(float(bal0), 'cyan')
        print('%s Balance : %s' % (coin0,bal0_))
        bal1_ = colored(float(bal1), 'blue')
        print('%s Balance: %s' % (coin1,bal1_))
        if debug: print("Difference: %.8f" % diff)
        buyTarget_=colored(float(buyTarget), 'green')
        print('Buy target : %s' %buyTarget_)
        sellTarget_=colored(float(sellTarget), 'red')
        print('Sell target : %s' %sellTarget_)
        print('Buy limit : %.8f' %(minPrice * 1.002))
        print('Sell limit : %.8f' %(maxPrice * 0.99))
        
        
        if bal0 > 0.001:
            if debug: print("DEBUG: Positive %s balance %s " % (coin0,bal0))
            if (lastPrice < buyTarget):
                if debug: print('DEBUG: lastPrice < buyTarget...')
                if (minPrice != 0) and (lastPrice > minPrice * 1.002):
                    print('DEBUG: minPrice is not 0')
                    buyAt = float(lastAsk * 1.0002)
                    if (lastPrice >= buyTarget):
                        if debug: print("DEBUG: minPrice greater than 0 and lastPrice > minPrice x min")
                        amt = (float(bal0) * 0.99)
                        
                        if verbose: print('Atemption to buy at %s ..' % buyAt)
                        if bal0 > 0.00005:
                            try:
                                data.buy(pair, lastPrice, amt)
                            except Exception as e:
                                print("Failed to buy with error : %s" % e)
                            else:
                                # since we just bought , try to make at least 5%
                                sellTarget = lastBid * 1.05
                                print(colored('Buy Price : %.8f'%lastPrice), 'red')
                                print('Buy price : %.8f' %lastPrice)
                                print(colored('Sell target : %.8f' %sellTarget), 'green')
                            minPrice = 0.0
                            maxPrice = 0.0
                else:
                        
                        if minPrice == 0:
                            minPrice = min(minPrice, lastPrice)
                        else:
                            minPrice = lastPrice
                
               
            else:
                minPrice = 0.0
                
        if bal1 > 0.0001:
            if debug: print("DEBUG: Positive %s balance: %s" % (coin1, bal1))
            diffPercent = percentage(lastAsk, lastBid)
            if debug: print ("DEBUG: Difference Percentage %.8f: " % diffPercent)
            amt = (bal1 * 0.99)
            # make at least a half a percent. logic needs work.
            if mode == "positive" and diffPercent >= 100.5:
                try:
                    data.sell(pair, sellTarget, amt)
                    amt1 = float(bal)
                    print(colored("Selling %s %s"% (amt1,coin1)), 'red')
                except Exception as lol:
                    if debug: print("DEBUG: %s" % lol)
                    sellTarget=str(sellTarget)
                    print(colored('Sell price : %s' %sellTarget), 'green')
                    sellTarget = 0.0
            else:
                if lastPrice > sellTarget:
                    if debug:print("DEBUG: lastprice is greater than selltarget")
                   
                    if sellTarget == 0.0:
                        sellTarget == (maxEMA * 1.05)
                    if debug: print("DEBUG maxPrice x 0.999: %.8f" % (maxPrice * 0.999))
                    if lastPrice < maxPrice:
                    
                        if debug: print("DEBUG: lastPrice less than sell price!")
                        if bal1 >= 0.00001:
                            if debug: print("DEBUG: MaxEMA : %.8f" % maxEMA)
                        

                            if verbose: print('INFO: Atemption to sell at %s ..' % sellTarget)
                            try:
                                data.sell(pair, sellTarget, amt)
                                amt1 = float(bal1)
                                print(colored("Selling %s %s"% (amt1,coin1)), "red")
                            except Exception as lol:
                                if debug: print("DEBUG: %s" % lol)
                            else:
                                sellTarget_ = colored(sellTarget, 'green')
                                print(colored('Sell price : %s' %sellTarget_), "green")
                                sellTarget = 0.0
                    else:
                        if verbose: print("INFO: Did not sell, %s less than %s" % (lastPrice,sellTarget))
                        maxPrice = max(maxPrice, lastPrice)
                else:
                    maxPrice = 0.0
        print('***************************************************')




        time.sleep(float(interval))

if __name__ == "__main__":
    print colored('Darkerego\'s', 'red'), colored('Trade Bot', 'green')
    main(sys.argv[1:])
