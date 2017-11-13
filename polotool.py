#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Poloniex API Wrapper ~ DarkerEgo 2017
#######################################
""" Skeleton for implimenting poloniex api functions """

import logging
import argparse
import time
import sys
####################
# Custom stuff here
####################
import poloniex
import json

pair = ''
key = ''
secret = ''
data = ''
hist = ''
debug = False



#

try:
        # For Python 3+
        from configparser import ConfigParser, NoSectionError
except ImportError:
        # Fallback to Python 2.7
        from ConfigParser import ConfigParser, NoSectionError
def main(argv):
        # Setup Argument Parser
        parser = argparse.ArgumentParser(description='Generic Parser')
        parser.add_argument('-c', '--config', default='polo.cfg', type=str, required=False, help='config .cfg file')
        parser.add_argument('-p', '--pair', default='null', type=str, required=False, help='Get ticker information for this pair (example: BTC_ETH)')
        parser.add_argument('-b', '--balances', default=False, action='store_true', required=False, help='Get ticker information for this pair (default: BTC_ETH)')
        parser.add_argument('-H', '--history', default='null', type=str, required=False, help='print market history data for given pair')
        parser.add_argument('-g',  '--gen_addr', default='null', type=str, required=False, help='Generate a new deposite address for supplied currency (example: BTC)')
        
        # parse args
        args = parser.parse_args()
        pair = args.pair
        balances = args.balances
        config = ConfigParser()
        hist = args.history
        gen_addr = args.gen_addr
        try:
                config.read(args.config)
                poloniexKey = config.get('bot', 'poloniexKey')
                poloniexSecret = config.get('bot', 'poloniexSecret')
                key = poloniexKey
                secret = poloniexSecret
                #if debug: print("%s : %s" % (key,secret))
        except NoSectionError:
                logger.warning('No Config File Found! Running in Drymode!')
                args.dryrun = True
                poloniexkey = 'POLONIEX_API_KEY'
                poloniexsecret = 'POLONIEX_API_SECRET'
                config.set('bot', 'poloniexKey', poloniexkey)
                config.set('bot', 'poloniexSecret', poloniexsecret)
        
       
                try:
                        with open(args.config, 'w') as configfile:
                                config.write(configfile)
                except IOError:
                        logger.error('Failed to create and/or write to {}'.format(args.config))
        # do stuff here
        data = poloniex.Poloniex(key,secret)
        
        if pair != 'null':
            ticker = data.returnTicker()
            print(ticker[pair])
        if balances:
            bal = data.returnAvailableAccountBalances('all')
            print(bal)
        if hist != 'null':
            if not pair:
                history = data.marketTradeHist(history)
                
            else:
                history = data.marketTradeHist(pair)
            for i in history:
                print(i)
        if gen_addr != 'null':
            ret = data.generateNewAddress(gen_addr)
            print(ret)
        

           



if __name__ == "__main__":
    main(sys.argv[1:])
