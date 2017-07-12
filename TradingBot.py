import datetime
import time
from poloniex import poloniex



def main():
	interval = 30
	pair = 'BTC_ETH'
	data = poloniex('', '')
	

	lastPrice = data.returnTicker()[pair]['last']
	while True:
		print '{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now()) + ' %s Last price : %s' % (pair, lastPrice)
		time.sleep(int(interval))
	
main()
