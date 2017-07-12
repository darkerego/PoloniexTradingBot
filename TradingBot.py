from poloniex import poloniex


def main():
	data = poloniex('', '')

	ret = data.returnTicker()

	
main()
