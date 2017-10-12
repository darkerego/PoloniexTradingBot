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




def main(argv):
	parser = argparse.ArgumentParser(description='Poloniex Trading Bot')
	parser.add_argument('-p', '--pair', default='BTC_ETH', type=str, required=False, help='Coin pair to trade between [default: BTC_ETH]')
	parser.add_argument('-i', '--interval', default=1, type=float, required=False, help='seconds to sleep between loops [default: 1]')
	parser.add_argument('-a', '--amount', default=1.01, type=float, required=False, help='amount to buy/sell [default: 1.01]')
	parser.add_argument('-v', '--verbose', action='store_true', required=False, help='enables extra console messages (for debugging)')
        parser.add_argument('-D', '--dry_run', action='store_true', required=False, help='Do not actually trade (for debugging)')
        parser.add_argument('-o', '--override', action='store_true', required=False, help='Sell anyway, do not wait to buy first. (for debugging)')

	args = parser.parse_args()

	sellTarget = 0.0
	minPrice = 0.0
	maxPrice = 0.0
	bought_at = 0.0
	bought_value = 0.0
	override = args.override
	if override:
            override = True
        else:
            override = False
	interval = args.interval
	pair = args.pair
	amt = args.amount
        amt = float(amt)
        dry = args.dry_run
        if dry:
            dry_run=True
        else:
            dry_run=False
        verbose = args.verbose
        if verbose:
            verbose = True
	cpair = pair.split('_')
	coin0 = cpair[0]
	coin1 = cpair[1]
        data = poloniex.Poloniex('', '')
	#demo = test()
	while True:
		chartClose = []
		timeNow = int(createTimeStamp('{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())))
		if timeNow % 900 != 0:
			timeNow = timeNow / 900 * 900
		lastPrice = float(data.returnTicker()[pair]['last'])
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
                    ema3 = data.returnChartData(pair,900, timeNow - 28800, timeNow)[-1]['weightedAverage']
                except:
                    pass
                if bought_at == 0:
		    buyTarget = min(ema1, ema2) * (amt * 0.98)
		    
		else:
                    buyTarget = bought_at * (amt * 0.98)
		    sellTarget = bought_at * amt
		try:
		    _bal = data.returnAvailableAccountBalances()['exchange'][coin0]
		except KeyError:
		    print('Likely balance is 0')
		    _bal = float(0.0)
		else:
		    _bal = float(_bal)

		try:
		    bal = data.returnAvailableAccountBalances()['exchange'][coin1]
		except KeyError:
		    if debug:
		        print('Likely balance is 0')
		    bal = float(0.0)
		else:
		    bal = float(bal)

		diff = (sellTarget - buyTarget)
		value = bal * lastPrice
                #value = str(value)
		pair_ = colored(str(pair), 'yellow')
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
                
                print('{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now()) + ' %s :' % (pair_))
                print('Last price : ')+ colored('%.8f' %(lastPrice), 'magenta',attrs=['blink'])
                #print('Current ask : ')+ colored('%.8f' %(lastAsk), 'blue')
                #print('Current bid : ')+ colored('%.8f' %(lastBid), 'cyan')
                print('EMA 1 : %.8f' %ema1)
                print('EMA 2 : %.8f' %ema2)
                print('EMA 3 : %s' %(ema3))
                print('%s Value : %.8f' %(coin1,value))
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
			if (float(lastPrice) <= float(buyTarget) * 0.99 ):
                                if verbose: print("DEBUG: %s lt %s" % (lastPrice,buyTarget))
                                #
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
                                                            data.buy(pair, (lastPrice * 1.0000001), amt_, orderType="postOnly")
                                                            bought_at = float(lastPrice)
                                                            bought_value = float(value)
                                                        except Exception as ee:
                                                            if verbose: print('Error: %s' % ee)
                                                        else:

                                                            sellTarget = bought_at * amt
                                                            sT = str(colored(sellTarget, 'red'))
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
		if bought_at != 0 or override or bal > 0.0001 or bought_value > value:
                        if verbose: print("Perhaps selling...")
                        if bought_at == 0:    
                            sellTarget = (max(ema1, ema2) * amt)
                        else:
                            sellTarget = bought_at * amt
		#else:
			if lastPrice >= sellTarget or bought_value > value:
				if (lastPrice < maxPrice * amt) or lastPrice >= (bought_at * amt):
                                        
                                        if dry_run:
                                            print("Not selling because dry_run is specified")
                                            pass
                                        else:
                                                if verbose: print(colored("Selling...", 'red'))
                                                try:
                                                    data.sell(pair, (lastPrice * 1.0000001), (bal * 0.99), orderType="postOnly")
                                                except Exception as lol:
                                                    lol = colored(lol, 'white')
                                                    print(colored("FATAL : %s", 'red')  % lol)
                                                    
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
        try:
	    main(sys.argv[1:])
	except KeyboardInterrupt:
            print("Caught Signal, exiting...")
            sys.exit(0)
