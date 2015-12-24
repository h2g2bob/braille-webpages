class BrailleChar(object):
	def __init__(self, numbers):
		assert numbers.isdigit()
		self.numbers = numbers
	def is_set(self, n):
		return str(n) in self.numbers
	def toggle(self, n):
		if n in self.numbers:
			return self.numbers.replace(n, '')
		else:
			l = self.numbers.split('') + [str(n)]
			return ''.join(sorted(l))
	def unicode(self):
		offset = 0
		for i in xrange(8):
			if self.is_set(i+1):
				offset += (1<<i)
		return unichr(0x2800 + offset)
