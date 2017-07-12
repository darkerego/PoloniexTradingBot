import datetime
import time
import poloniex
from poloniex import poloniex

def createTimeStamp(datestr, format="%Y-%m-%d %H:%M:%S"):
    return time.mktime(time.strptime(datestr, format))

def sum(array):
	ret = 0.0
	for x in array:
		ret += x
	return ret

def main():
	interval = 30
	pair = 'BTC_ETH'
	data = poloniex('', '')
	while True:
		chartClose = []
		timeNow = int(createTimeStamp('{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())))
		lastPrice = data.returnTicker()[pair]['last']
		chartData = data.returnChartData(pair, timeNow - 28800, timeNow, 900)
		for candle in chartData:
			chartClose.append(candle['close'])
		ema1 = sum(chartClose[0:16]) / 16
		ema2 = sum(chartClose[16:24]) / 8
		for i in range(16,32):
			ema1 += (chartClose[i] - ema1) * 2 / 17
		for i in range(24,32):
			ema2 += (chartClose[i] - ema2) * 2 / 9

		#ema2 = data.returnChartData(pair, timeNow - 7200, timeNow, 900)[-1]['weightedAverage']
		print '{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now()) + ' %s :' % (pair)
		print 'Last price : %s' %(lastPrice)
		print 'EMA 1 : %s' %ema1
		print 'EMA 2 : %s' %ema2

		time.sleep(int(interval))
	
main()
