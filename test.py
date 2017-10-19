""" For example/historical/educational/testing/development usage. Does not actually do anything. """

class test():
	btc = 1.0
	alt = 0.0
	fee = 0.005

	def balance(self):
		return self.btc

	def buy(self, price):
		self.alt = (self.btc / price) * (1 - self.fee)
		self.btc = 0
		return 0

	def sell(self, price):
		self.btc = self.alt * price
		self.alt = 0
		return 0

	def value(self, price):
		return self.btc + self.alt * price
