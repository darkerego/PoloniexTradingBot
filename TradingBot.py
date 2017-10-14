#!/usr/bin/env python
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

import poloniex
from termcolor import colored
#from poloniex import poloniex
#from test import test
debug = False
def createTimeStamp(datestr, format="%Y-%m-%d %H:%M:%S"):
    return time.mktime(time.strptime(datestr, format))

def sum(array):
	ret = float(0.0)
	for x in array:
		x = float(x)
		#ret = float(ret)
		ret += x
	return ret



secret = False # change to your api key
key = False # change to your api secret

def main(argv):
if not secret and key:
    print("First you must edit me and set your api key!")
    sys.exit(1)

	parser = argparse.ArgumentParser(description='Poloniex Trading Bot')
	parser.add_argument('-p', '--pair', default='BTC_ETH', type=str, required=False, help='Coin pair to trade between [default: BTC_ETH]')
	parser.add_argument('-i', '--interval', default=1, type=float, required=False, help='seconds to sleep between loops [default: 1]')
	parser.add_argument('-a', '--amount', default=1.01, type=float, required=False, help='amount to buy/sell [default: 1.01]')
	parser.add_argument('-v', '--verbose', action='store_true', required=False, help='enables extra console messages (for debugging)')
        parser.add_argument('-D', '--dry_run', action='store_true', required=False, help='Do not actually trade (for debugging)')
        parser.add_argument('-o', '--override', action='store_true', required=False, help='Sell anyway, do not wait to buy first. (for debugging)')
        parser.add_argument('-u', '--usdt_anchor', action='store_true', required=False, help='Attempt to buy/sell from/to usdt when oppurtune, default=False') # not yet implemented

	args = parser.parse_args()
        bought = False
	sellTarget = 0.0
	minPrice = 0.0
	maxPrice = 0.0
	bought_at = 0.0
	lastAsk = 0.0
	lastBid = 0.0
	btc_value = 0.0
	btc_value_ = 0.0
	lastAsk_usdt = 0.0
	
	lastPrice_usdt = 0.0
	lastPrice_usdt_ = 0.0
	lastAsk_usdt_ = 0.0
	bought_value = 0.0
	usdt_value = 0.0
	usdt_anchor=False
        if usdt_anchor:
            usdt_anchor = True
        
	override = args.override
	if override:
            override = True
        else:
            override = False
	interval = args.interval
	pair = args.pair
	
	amt = args.amount
        amt = float(amt)
        _amt = 100 - (amt * 100)
        amt_buy = (100 + _amt) * 0.01
        
        dry = args.dry_run
        if dry:
            dry_run=True
        else:
            dry_run=False
        verbose = args.verbose
        if verbose:
            verbose = True
        else:
            verbose=False
	cpair = pair.split('_')
	coin0 = cpair[0]
	coin1 = cpair[1]
	cpair_usdt = "USDT"+"_"+str(cpair[1])
	cpair_usdt_ = "USDT"+"_"+str(cpair[0])
	cpair_btc = "BTC"+"_"+str(cpair[1])
	cpair_btc_ = "BTC"+"_"+str(cpair[0])
	
	pair_ = cpair_usdt
	print(colored("Darkerego's Trade bot", 'red', attrs=['dark']))
	print(colored("Buy percent: %s" % amt_buy, 'green'))
        print(colored("Sell percent: %s" % amt, 'red'))
        data = poloniex.Poloniex(secret, key)
	#demo = test()
	while True:
		chartClose = []
		timeNow = int(createTimeStamp('{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())))
		if timeNow % 900 != 0:
			timeNow = timeNow / 900 * 900
		ticker = data.returnTicker()
		lastPrice = float(ticker[pair]['last'])
		lastPrice_ = float(ticker[pair_]['last'])
		#

		chartData = data.returnChartData(pair, 900, timeNow - 28800, timeNow)
		for candle in chartData:
			chartClose.append(candle['close'])
			#if debug:
			    #print(chartClose)
		
		ema1 = sum(chartClose[0:16]) / 16
		#ema1 = float(ema1)
		
		if debug:
 		    print("ema1: "+str(ema1))
		ema2 = sum(chartClose[16:24]) / 8
		for i in range(16,32):
                        try:
			    chartClose[i] = float(chartClose[i])
			except IndexError:
                            if verbose: print(colored("FATAL! Chart data out of range!", 'red'))
                            pass
                        try:
			    ema1 += (chartClose[i] - ema1) * 2 / 17
			except IndexError:
                             if verbose: print(colored("FATAL! Chart data out of range!", 'red'))
                             pass
		for i in range(24,32):
                        try:
			    ema2 += (chartClose[i] - ema2) * 2 / 9
			except IndexError:
                             if verbose: print(colored("FATAL! Chart data out of range!", 'red'))
                             pass
		try:
                    #ema3 = data.returnChartData(pair,900, timeNow - 28800, timeNow)[-1]['weightedAverage']
                    ema3 = chartData[-1]['weightedAverage']
                except:
                    pass
                if bought_at == 0.0:
                    #if debug: print("No buys yet")
		    buyTarget = min(ema1, ema2) * amt_buy
		    
		else:
                    #print(bought_at)
                    buyTarget = bought_at * amt_buy
		    sellTarget = bought_at * amt
                try:
                    bals = data.returnAvailableAccountBalances()
                except Exception as e:
                    print(colored("FATAL: Cannot get balances!"), 'red')
                    
		try:
		    _bal = bals['exchange'][coin0]
		except KeyError:
                    if debug: print('Likely balance is 0')
		    _bal = float(0.0)
		else:
		    _bal = float(_bal)

		try:
		    bal = bals['exchange'][coin1]
		except KeyError:
		    if debug: print('Likely balance is 0')
		    bal = float(0.0)
		else:
		    bal = float(bal)
		    
		try:
                    bal_usdt = bals['exchange']['usdt']
                except KeyError:
                    if debug: print('Likely balance is 0')
		    bal_usdt = float(0.0)
		else:
		    bal_usdt = float(bal_usdt)
		    
                try:
                    orders = data.returnOrderBook()
                    orderBook = orders(pair)
                    
                    lastAsk = orders['asks'][0]
                    lastBid = orders['bids'][0]
                    lastAsk = float(lastAsk[0])
                    lastBid = float(lastBid[0])
                    orderBook_ = orders(pair_)
                    lastAsk_ = orders['asks'][0]
                    lastBid_ = orders['bids'][0]
                    lastAsk_ = float(lastAsk[0])
                    lastBid_ = float(lastBid[0])
                    
                except:
                    pass
                
                lastAsk_usdt = float(ticker[cpair_usdt]['last'])
                lastBid_usdt = float(ticker[cpair_usdt]['highestBid'])
                lastAsk_usdt_ = float(ticker[cpair_usdt_]['last'])
                lastBid_usdt_ = float(ticker[cpair_usdt_]['highestBid'])
                lastAsk_btc = float(ticker[cpair_btc]['last'])
                lastAsk_btc_ = float(ticker[cpair_btc_]['last'])

                btc_value = lastAsk_btc * bal
                btc_value_ = lastAsk_btc_ * _bal
                usdt_value_ = lastAsk_usdt_ * _bal
                usdt_diff_ = lastPrice_usdt_ - lastBid_usdt_
                usdt_diff = lastPrice_usdt - lastBid_usdt
                usdt_value = lastAsk_usdt * bal
		diff = (sellTarget - buyTarget)
		value = bal * lastPrice
                #value = str(value)
		pair__ = colored(str(pair), 'yellow')
		"""
		print('{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now()) + ' %s :' % (pair))
		print('Last price : %.8f' %(lastPrice))
		print('EMA 1 : %.8f' %ema1)
		print('EMA 2 : %.8f' %ema2)
                print('EMA 3 : %s' %(ema3))
		print('Value : %.8f' %(value))
		print('%s Balance : %.8f' % (coin0,_bal))
		print('%s Balance: %.8f' % (coin1,bal))
		print('Buy target : %.8f' %buyTarget)
		print('Sell target : %.8f' %sellTarget)
		print('Buy limit : %.8f' %(minPrice * 1.002))
		print('Sell limit : %.8f' %(maxPrice * 0.999))
		"""
                
                print('{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now()) + ' %s :' % (pair__))
                print('Last price : ')+ colored('%.8f' %(lastPrice), 'magenta',attrs=['blink'])
                print('Current ask : ')+ colored('%.8f' %(lastAsk), 'blue',attrs=['dark'])
                print('Current bid : ')+ colored('%.8f' %(lastBid), 'cyan',attrs=['dark'])
                print('Last price usdt : ')+ colored('%.8f' %(lastPrice_), 'magenta',attrs=['blink'])
                print('Current ask usdt: ')+coin1+" "+colored('%.8f' %(lastAsk_usdt), 'green',attrs=['dark'])
                print('Current bid usdt: ')+coin1+" "+ colored('%.8f' %(lastBid_usdt), 'cyan',attrs=['dark'])
                print('USDT Difference: %.8f' % usdt_diff)
                strusdt_value = str(usdt_value)
                print('USDT Value: %s : %s' % (coin1, strusdt_value))
                strusdt_value_ = str(usdt_value_)
                print('USDT Value: %s : %s' % (coin0, strusdt_value_))
                strbtc_value = str(btc_value)
                print('BTC Value: %s : %s ' % (coin1, strbtc_value))
                strbtc_value_ = str(btc_value_)
                print('BTC Value: %s : %s ' % (coin0, strbtc_value_))
                
                
                print('EMA 1 : %.8f' %ema1)
                print('EMA 2 : %.8f' %ema2)
                print('EMA 3 : %s' %(ema3))
                print('%s Value : %.8f' %(coin1,value))
                
                usdt_bal = colored(float(bal_usdt), 'cyan', attrs=['dark'])
                print("USDT Balance: %s " % usdt_bal)
                bal0_ = colored(float(_bal), 'cyan')
                print('%s Balance : %s' % (coin0,bal0_))
                bal1_ = colored(float(bal), 'blue')
                print('%s Balance: %s' % (coin1,bal1_))
                if verbose: print("Difference: %.8f" % diff)
                buyTarget_=colored(float(buyTarget), 'green')
                print('Buy target : %s' %buyTarget_)
                if bought_at != 0 :
                    bought_at_ = colored(bought_at, 'green', attrs=['dark'])
                    print("Bought at : %s " % bought_at_)
                if bought_value:
                   bought_value_ = colored(bought_at, 'yellow', attrs=['dark'])
                   print("Bought value : %s " % bought_value_)
                    
                sellTarget_=colored(float(sellTarget), 'red')
                print('Sell target : %s' %sellTarget_)
                print('Buy limit : %.8f' %(minPrice * 0.99))
                print('Sell limit : %.8f' %(maxPrice * 0.99))
		
		if _bal > 0.0001:
			if (float(lastPrice) <= float(buyTarget) * amt_buy ):
                                if verbose: print("DEBUG: %s lt %s" % (lastPrice,buyTarget))
                                minPrice = min(minPrice, lastPrice)
                                if dry_run:
                                     print("Not buying because dry_run is specified")
                                     pass
                                
                                else:
                                        
                                        if (minPrice != 0) and (lastPrice > minPrice):
                                                if verbose: print("Attempting to buy...")
                                                
                                                if _bal > 0:
                                                    if not dry_run:
                                                        if verbose: print(colored("Buying...",'green'))
                                                        try:
                                                            amt_ = float(_bal) / float(lastPrice) * 0.99
                                                            if dry_run:
                                                                
                                                                print("Not buying because dry_run is specified")
                                                                bought_at = float(lastPrice *  1.0000001)
                                                                bought_value = float(value)
                                                                bought = True 
                                                                pass
                                                            else:
                                                                data.buy(pair, (lastPrice * 1.0000001), amt_, orderType="postOnly")
                                                                bought_at = float(lastPrice)
                                                                bought_value = float(value)
                                                        except Exception as ee:
                                                            if verbose: print('Error: %s' % ee)
                                                        else:

                                                            sellTarget = bought_at * amt
                                                            sT = str(colored(sellTarget, 'red'))
                                                            if bought:
                                                                print(colored("Bought! Sell Target: %s" % sT, 'green'))
                                                            minPrice = 0.0
                                                            maxPrice = 0.0
                                                            print('Buy price : %.8f' %lastPrice)
                                                            print('Sell target : %.8f' %sellTarget)
                                        else:
                                                if verbose: print("Not buying...")
                                                
                                                if minPrice != 0:
                                                        minPrice = min(minPrice, lastPrice)
                                                else:
                                                        minPrice = lastPrice
			else:
				minPrice = 0.0
		#if bought_at != 0 or override or bal > 0.00001 or bought_value > value or bought:
		else:
                       
                        if bought_at == 0:    
                            sellTarget = (max(ema1, ema2) * amt)
                        else:
                            sellTarget = bought_at * amt
		#else:
			if lastPrice >= sellTarget or bought_value > value:
                                if verbose: print("Perhaps selling...")
				if (lastPrice < maxPrice * (amt * 0.999)) or lastPrice >= (bought_at * amt):
                                        
                                        if dry_run:
                                            print("Not selling because dry_run is specified")
                                            pass
                                        else:
                                                if verbose: print(colored("Selling...", 'red'))
                                                try:
                                                    data.sell(pair, (lastPrice * 1.0000001), (bal * 0.99), orderType="postOnly")
                                                except Exception as lol:
                                                    lol = colored(lol, 'white')
                                                    if verbose: print(colored("FATAL ERROR SELLING :", 'red'))
                                                    if verbose: print(lol)
                                                    
                                                else:
                                                    print('Sell price : %.8f' %lastPrice)
                                                    sellTarget = 0.0
				else:
					maxPrice = max(maxPrice, lastPrice)
			else:
				maxPrice = 0.0
		print('***************************************************')



                try:
		     time.sleep(int(interval))
		except KeyboardInterrupt:
                     print("Caught Signal, exiting...")
                     sys.exit(0)
                     
if __name__ == "__main__":
        while True:
            try:
	        main(sys.argv[1:])
	    except KeyboardInterrupt:
                print("Caught Signal, exiting...")
                sys.exit(0)
