# TradingBot


<p> I have made some improvements to the initial code. I am still not certain if this this bot actually makes money or not. </p>
<p> You need the real poloniex api, get it from here: https://github.com/darkerego/python-poloniex </p>


python TradingBot44.py -h
Darkerego's Trade Bot
usage: TradingBot44.py [-h] [-p PAIR] [-i INTERVAL] [-b AMOUNT_BUY]
                       [-s AMOUNT_SELL] [-v] [-m MODE] [-d]

Poloniex Trading Bot

optional arguments:
  -h, --help            show this help message and exit
  -p PAIR, --pair PAIR  Coin pair to trade between [default: BTC_ETH]
  -i INTERVAL, --interval INTERVAL
                        seconds to sleep between loops [default: 1]
  -b AMOUNT_BUY, --amount_buy AMOUNT_BUY
                        percentage of balances to buy/sell [default: 0.99]
  -s AMOUNT_SELL, --amount_sell AMOUNT_SELL
                        percentage of balances to buy/sell [default: 1.02]
  -v, --verbose         enables verbose console messages
  -m MODE, --mode MODE  mode: positive (smaller propfit more often) or normal
  -d, --debug           enables extra console messages (for debugging)
