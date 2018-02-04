#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-
# Poloniex API Wrapper ~ DarkerEgo 2017
#######################################

from __future__ import print_function
import logging
import argparse
import time
import sys
####################
# Custom stuff here
####################
import poloniex
import json
#
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG, filename='polo-tool.log')
all_balance=''
pair = ''
key = ''
secret = ''
data = ''
hist = ''
debug = False
buysell_err = str('Please specify options: -p/--pair [ex: BTC_ETH] -P/--price [ex: 0.05] -a/--amount [ex: 0.25]')


def timeStamp():
     return time.time()

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

#

try:
        # For Python 3+
        from configparser import ConfigParser, NoSectionError
except ImportError:
        # Fallback to Python 2.7
        from ConfigParser import ConfigParser, NoSectionError
def main(argv):
        # Setup Argument Parser
        parser = argparse.ArgumentParser(description='Poloniex API Tool')
        parser.add_argument('-c', '--config', default='./polo.cfg', type=str, required=False, help='config .cfg file')
        parser.add_argument('-p', '--pair', default='null', type=str, required=False, help='Get ticker information for this pair (example: BTC_ETH)')
        parser.add_argument('-B', '--balances', default=False, action='store_true', required=False, help='Get available balances')
        #returnCompleteBalances
        parser.add_argument('-A', '--all_balance', default=False, action='store_true', required=False, help='Get all balance data')
        parser.add_argument('-H', '--history', default=False, action='store_true', required=False, help='print market history data for given pair ,specify w -p')
        parser.add_argument('-g',  '--gen_addr', default='null', type=str, required=False, help='Generate a new deposite address for supplied currency (example: BTC)')
        parser.add_argument('-t', '--ticker', default=False, action='store_true', required=False, help='Get ticker information for pai , specify with -p (default: BTC_ETH)')
        #
        parser.add_argument('-b', '--buy', default=False, action='store_true', required = False, help='Buy ')
        parser.add_argument('-s', '--sell', default=False, action='store_true', required = False, help='Sell ')
        parser.add_argument('-a', '--amount', default='0.0', type=float, required=False, help='Amount to buy or sell')
        parser.add_argument('-P','--price', default='0.0', type=float , required=False, help="Price to buy or sell at")
        parser.add_argument('-o','--orders', default=False, action='store_true', required=False, help="Return open orders")
        parser.add_argument('-C', '--cancel_order', default=False, action='store_true' ,required=False, help="Cancel an order")
        parser.add_argument('-m', '--move_order', default=False, action='store_true', required=False, help="Move an order")
        parser.add_argument('-i', '--order_id', type=str, default='null',required=False, help="Cancel an order")

        # parse args
        args = parser.parse_args()
        pair = args.pair
        all_balance = args.all_balance
        balances = args.balances
        config = ConfigParser()
        hist = args.history
        gen_addr = args.gen_addr
        move_order = args.move_order
        #all_balance = args.all_balance
        #
        buy = args.buy
        sell = args.sell
        amount = args.amount
        ticker = args.ticker
        price = args.price
        orders = args.orders
        cancel_order = args.cancel_order
        order_id = args.order_id

        try:
                config.read(args.config)
                poloniexKey = config.get('bot', 'poloniexKey')
                poloniexSecret = config.get('bot', 'poloniexSecret')
                key = poloniexKey
                secret = poloniexSecret
                #if debug: print("%s : %s" % (key,secret))
        except NoSectionError:
                print('No Config File Found! Running in Drymode!')
                args.dryrun = True
                poloniexkey = 'POLONIEX_API_KEY'
                poloniexsecret = 'POLONIEX_API_SECRET'
                config.set('bot', 'poloniexKey', poloniexkey)
                config.set('bot', 'poloniexSecret', poloniexsecret)
        
       
                try:
                        with open(args.config, 'w') as configfile:
                                config.write(configfile)
                except IOError:
                        eprint('Failed to create and/or write to {}'.format(args.config))
        # do stuff here
        tS = timeStamp()
        data = poloniex.Poloniex(key,secret)
        logging.debug("Program started at %s" % tS)
        if ticker and pair != 'null':
            ticker = data.returnTicker()
            # this fixes json!
            ret = json.dumps(ticker[pair])
            logging.info("Ticker call: "+ret)
            print(ret)
        if ticker and pair == 'null':
            print('Specify a pair with -p')
            sys.exit(1)
        if move_order:
            if order_id == 'null' or pair == 'null' or float(price) <= float('0.0') or float(amount) <= float('0.0'):
                print("Specifiy an order id <-> , price <-P> , pair <-> , and amount <-a>")
                sys.exit(1)
            else:
                try:
                    ret = data.moveOrder(order_id, price, amount)
                except Exception as err:
                    logging.info(err)
                    eprint(err)
                    sys.exit(1)
                else:
                    ret = json.dumps(ret)
                    logging.info(ret)
                    print(ret)
                    sys.exit(0)
        if all_balance:
            bals = data.returnCompleteBalances('all')
            bret = json.dumps(bals)
            logging.info("All balances call : "+str(bret))
            print(bret)
        if balances:
            bal = data.returnAvailableAccountBalances('all')
            ret = json.dumps(bal)
            logging.info("Balance call: "+ret)
            print(ret)
        if hist:
            if not pair:
                history = data.returnTradeHistory()
                logging.info("History call. Not logging that much data.")
                for i in history:
                     print("%s\n" % i)
               
            else:
                history = data.returnTradeHistory(pair)
                logging.info("History call. Not logging that much data.")
                for i in history:
                    print("%s\n" % i)
                    #print(i)
        if gen_addr != 'null':
            ret = data.generateNewAddress(gen_addr)
            ret = json.dumps(ret)
            logging.info("Generate Deposit address called: "+ret)
            print(ret)

        if buy:
            if pair != 'null':
                if float(price) > 0.0:
                    if float(amount) > 0.0:
                        try:
                          ret = data.buy(pair, price, amount)
                          #logging.info("Buy order call: "+ret)
                          #print(ret)
                        except Exception as err:
                            eprint(err)
                            sys.exit(1)
                        else:
                          if debug: eprint(ret)
                          ret = json.dumps(ret)
                          ret_ = str(ret)
                          logging.info("Buy order call: "+ret_)
                          print(ret)
                          sys.exit(0)
                    else:
                        eprint(buysell_err)
                        sys.exit(1)
                else:
                    eprint(buysell_err)
                    sys.exit(1)

            else:
                eprint(buysell_err)
                sys.exit(1)



        if sell:
            if pair != 'null':
                if float(price) > 0.0:
                    if float(amount) > 0.0:
                        try:
                            ret = data.sell(pair, price, amount)
                        except Exception as err:
                            eprint(err)
                            sys.exit(1)
                        else:  
                          ret = json.dumps(ret)
                          if debug: eprint(ret)
                          ret_ = str(ret)
                          logging.info("Sell order call: "+ret_)
                          print(ret)
                          sys.exit(0)
                    else:
                        eprint(buysell_err)
                        sys.exit(1)
                else:
                    eprint(buysell_err)
                    sys.exit(1)
            else:
                eprint(buysell_err)
                sys.exit(1)


        if orders:
            try:
                ret = data.returnOpenOrders('all')
            except Exception as err:
                eprint(err)
                sys.exit(1)
            else:
                ret = json.dumps(ret)
                logging.info("Open orders call: " +ret)
                print(ret)
                    
        if cancel_order:
            if order_id != 'null':
                try:
                    ret = data.cancelOrder(order_id)
                except Exception as err:
                    eprint(err)
                    return False
                else:
                    ret = json.dumps(ret)
                    logging.info("Cancel order call: "+ret)
                    print(ret)
            else:
                eprint("Please specify order id with -i <order id>")
                sys.exit(1)




if __name__ == "__main__":
    main(sys.argv[1:])
