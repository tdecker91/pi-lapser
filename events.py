import math

class RepeatingEvent(object):

	def __init__(self, started, interval):
		self.last = started
		self.interval = interval

	def next(self):
		self.last = self.last + self.interval
		return self.last