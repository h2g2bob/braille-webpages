class BrailleChar(object):
	def __init__(self, numbers):
		assert numbers.isdigit()
		self.numbers = numbers

	def is_set(self, n):
		return str(n) in self.numbers

	def toggle(self, n):
		n = str(n)
		if n in self.numbers:
			return self.numbers.replace(n, '') or '0'
		else:
			l = list(self.numbers.replace('0', '')) + [str(n)]
			return ''.join(sorted(l))

	@property
	def unicode(self):
		return unichr(self.unicode_number)

	@property
	def unicode_number_hex(self):
		return "%04x" % (self.unicode_number,)

	@property
	def unicode_number(self):
		offset = 0
		for i in xrange(8):
			if self.is_set(i+1):
				offset += (1<<i)
		return 0x2800 + offset

	@property
	def decade(self):
		if self.is_8_dot():
			return 'Extended (8-dot)'
		elif not self.is_set('1') and not self.is_set('4'):
			return '5th decade'
		elif self.is_set('3') and self.is_set('6'):
			return '3rd decade'
		elif self.is_set('6'):
			return '4th decade'
		elif self.is_set('3'):
			return '2nd decade'
		else:
			return '1st decade'

	def is_8_dot(self):
		return self.is_set('7') or self.is_set('8')
