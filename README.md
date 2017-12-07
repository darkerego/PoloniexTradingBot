# Poloniex TradingBot

<i>This is a Proof of <s>Concept</s> Crap [honestly], still in development, do not use in production with lots money! </i> 

<p> I have made some improvements to the initial code. I am still not certain if this this bot actually makes money or not. </p>
<p> Update: Added some static python function/files to do things like get balances, generate new deposite addresses, grab your trade history, and get the current market charts. They are 'extras' and are not used in the actual TradingBot.py program.</p>
<p> Update: The bot does profit in upward trending markets, so that is a good start. </p>

### Project Goals:

- To create a poloniex trading bot that uses simple math to trade across poloniex's btc and usdt markets. 
- Create a poloniex api wrapper tool (to generate a new deposite address, or grab balances, etc)
- In progress: Finish creating (a) function(s) that checks if at any given moment it is profitable to buy from a usdt market and sell to btc market
 - or vice versa, this also should work on other markets such as ETH/ETC or LTC/XMR , say buy from BTC/ETH when it's cheaper

### Usage:

<p> First, create a poloniex API key and add your secret and key to the config file `api_conf.py`. </p>
<p> Next, install the requirements: </p>
<p> (You need the good poloniex api : [https://github.com/s4w3d0ff/python-poloniex] and termcolor, see the requirements.txt.)  </p>

<pre>
pip install -r requirements.txt
</pre>
<p> Finally, try a dry run to see the bot in action </p>
<pre>
python TradingBot.py -D
</pre>

###### Sample Run:

<img src="https://s1.postimg.org/22ad73qgtr/botsample-new.png"></img>


<pre>
python TradingBot.py -h
usage: TradingBot.py [-h] [-p PAIR] [-i INTERVAL] [-a AMOUNT] [-f FEE] [-v]
                        [-D] [-o] [-u] [-b]

Poloniex Trading Bot

optional arguments:
  -h, --help            show this help message and exit
  -p PAIR, --pair PAIR  Coin pair to trade between [default: BTC_ETH]
  -i INTERVAL, --interval INTERVAL
                        seconds to sleep between loops [default: 1]
  -a AMOUNT, --amount AMOUNT
                        amount to buy/sell [default: 1.01]
  -f FEE, --fee FEE     Taker fee to calculate into buys/sells [default:
                        1.0015 (.15 percent)]
  -v, --verbose         enables extra console messages (for debugging)
  -D, --dry_run         Do not actually trade (for debugging)
  -o, --override        Sell anyway, do not wait to buy first. (for debugging)
  -u, --usdt_anchor     Attempt to buy/sell from/to usdt when oppurtune,
                        default=False
  -b, --btc_tether      Attempt to buy/sell to markets when possible


</pre>

###### Polotool

<pre>
python3 polotool.py -h
usage: polotool.py [-h] [-c CONFIG] [-p PAIR] [-b] [-H HISTORY] [-g GEN_ADDR]

Generic Parser

optional arguments:
  -h, --help            show this help message and exit
  -c CONFIG, --config CONFIG
                        config .cfg file
  -p PAIR, --pair PAIR  Get ticker information for this pair (example:
                        BTC_ETH)
  -b, --balances       Get account balances 
  -H HISTORY, --history HISTORY
                        print market history data for given pair
  -g GEN_ADDR, --gen_addr GEN_ADDR
                        Generate a new deposite address for supplied currency
                        (example: BTC)
</pre>

