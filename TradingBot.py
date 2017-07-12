import datetime
import time
import poloniex
from poloniex import poloniex

def createTimeStamp(datestr, format="%Y-%m-%d %H:%M:%S"):
    return time.mktime(time.strptime(datestr, format))

def main():
	interval = 30
	pair = 'BTC_ETH'
	data = poloniex('', '')
	chartData = data.returnChartData(pair, timeNow - 14400, timeNow, 900)
	for candle in chartData:
		chartClose.append(candle['close']) 

	while True:

		timeNow = int(createTimeStamp('{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())))
		lastPrice = data.returnTicker()[pair]['last']
		chartData = data.returnChartData(pair, timeNow - 14400, timeNow, 900)
		for candle in chartData:
			chartClose.append 
		#ema2 = data.returnChartData(pair, timeNow - 7200, timeNow, 900)[-1]['weightedAverage']
		print '{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now()) + ' %s :' % (pair)
		print 'Last price : %s' %(lastPrice)
		print 'EMA 1 : %s' %ema1
		#print 'EMA 2 : %s' %ema2

		time.sleep(int(interval))
	
main()
