import datetime
import time
import poloniex
from poloniex import poloniex
from test import test

def createTimeStamp(datestr, format="%Y-%m-%d %H:%M:%S"):
    return time.mktime(time.strptime(datestr, format))

def sum(array):
	ret = 0.0
	for x in array:
		ret += x
	return ret

def main():
	sellTarget = 0.0
	minPrice = 0.0
	interval = 30
	pair = 'BTC_ETC'
	data = poloniex('', '')
	demo = test()
	while True:
		chartClose = []
		timeNow = int(createTimeStamp('{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())))
		if timeNow % 900 != 0:
			timeNow = timeNow / 900 * 900
		lastPrice = float(data.returnTicker()[pair]['last'])
		chartData = data.returnChartData(pair, timeNow - 28800, timeNow, 900)
		for candle in chartData:
			chartClose.append(candle['close'])
		ema1 = sum(chartClose[0:16]) / 16
		ema2 = sum(chartClose[16:24]) / 8
		for i in range(16,32):
			ema1 += (chartClose[i] - ema1) * 2 / 17
		for i in range(24,32):
			ema2 += (chartClose[i] - ema2) * 2 / 9
		buyTarget = (min(ema1, ema2) * 0.99)
		#ema2 = data.returnChartData(pair, timeNow - 7200, timeNow, 900)[-1]['weightedAverage']
		print '{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now()) + ' %s :' % (pair)
		print 'Last price : %s' %(lastPrice)
		print 'EMA 1 : %s' %ema1
		print 'EMA 2 : %s' %ema2
		print 'Value : %s' %demo.value(lastPrice)
		print 'Balance : %s' %demo.balance()
		print 'Buy target : %s' %buyTarget
		print 'Sell target : %s' %sellTarget
		if demo.balance() > 0:
			if (lastPrice < buyTarget):
				if (minPrice != 0) & (lastPrice > minPrice * 1.01):
					demo.buy((lastPrice))
					sellTarget = lastPrice * 1.01
					minPrice = 0.0
					maxPrice = 0.0
					print 'Buy price : %s' %lastPrice
					print 'Sell target : %s' %sellTarget
				else:
					if minPrice != 0:
						minPrice = min(minPrice, lastPrice)
					else:
						minPrice = lastPrice
			else:
				minPrice = 0.0
		else:
			if lastPrice > sellTarget:
				if lastPrice < maxPrice * 0.999:
					demo.sell(lastPrice)
					print 'Sell price : %s' %lastPrice
					sellTarget = 0.0
				else:
					maxPrice = max(maxPrice, sellTarget)
			else:
				maxPrice = 0.0
		print '***************************************************'




		time.sleep(int(interval))
	
main()
