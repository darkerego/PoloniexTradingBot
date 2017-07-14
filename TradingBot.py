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
	maxPrice = 0.0
	interval = 30
	pair = 'BTC_LTC'
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
		print 'Last price : %.8f' %(lastPrice)
		print 'EMA 1 : %.8f' %ema1
		print 'EMA 2 : %.8f' %ema2
		print 'Value : %.8f' %demo.value(lastPrice)
		print 'Balance : %.8f' %demo.balance()
		print 'Buy target : %.8f' %buyTarget
		print 'Sell target : %.8f' %sellTarget
		print 'Buy limit : %.8f' %(minPrice * 1.002)
		print 'Sell limit : %.8f' %(maxPrice * 0.999)
		if demo.balance() > 0:
			if (lastPrice < buyTarget):
				if (minPrice != 0) & (lastPrice > minPrice * 1.002):
					demo.buy((lastPrice))
					sellTarget = lastPrice * 1.01
					minPrice = 0.0
					maxPrice = 0.0
					print 'Buy price : %.8f' %lastPrice
					print 'Sell target : %.8f' %sellTarget
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
					print 'Sell price : %.8f' %lastPrice
					sellTarget = 0.0
				else:
					maxPrice = max(maxPrice, lastPrice)
			else:
				maxPrice = 0.0
		print '***************************************************'




		time.sleep(int(interval))
	
main()
