class test():
	btc = 1.0
	alt = 0.0

	def buy(self, price):
		self.alt = self.btc / price
		self.btc = 0
		return 0

	def sell(self, price):
		self.btc = self.alt * price
		self.alt = 0
		return 0

	def value(self, price):
		return self.btc + self.alt * price
