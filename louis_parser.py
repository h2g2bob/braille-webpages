import logging
from collections import defaultdict, namedtuple
from pprint import pprint
import sys

# TABLE='/usr/share/liblouis/tables/en-GB-g2.ctb'
TABLE='/usr/share/liblouis/tables/en-gb-g1.utb'

# http://liblouis.org/documentation/liblouis.html

Word = namedtuple('Word', 'table pattern abc_word comment')

WORDS = {'always', 'begword', 'word', 'midendword', 'joinword', 'sufword', 'lowword', 'midword', 'endword', 'endnum', 'largesign', 'begnum', 'sign', 'litdigit', 'joinnum', 'midnum', 'uplow', 'prepunc', 'postpunc', 'decpoint', 'multind', 'letter', 'hyphen', 'punctuation'}

FORMATTING = {'begital', 'endital', 'begbold', 'endbold', 'begcaps', 'endcaps', 'capsign', 'numsign', 'letsign', 'begcomp', 'endcomp'}

IGNORE = {'literal', 'include', 'repeated', 'contraction'}

class DotLetter(object):
	def __init__(self):
		self.things = {w : [] for w in WORDS | FORMATTING}
	def __repr__(self):
		return 'DotLetter(%r)' % (self.__dict__,)

def parse_table(table):
	dot_letters = defaultdict(DotLetter)

	with open(table) as f:
		for line in f:
			tokens = line.strip().split()

			if not tokens:
				continue
			if tokens[0].startswith('#'):
				continue

			if tokens[0] in IGNORE:
				continue

			elif tokens[0] in FORMATTING:
				abc_word = tokens[1]
				if tokens[2:]:
					comment = 'For example, in %s' % (', '.join(tokens[2:]))
				else:
					comment = ''
				dot_word = ''

				word = Word(table, dot_word, abc_word, comment)
				for dot in split_dot_word(dot_word):
					dot_letters[dot].things[tokens[0]].append(word)

			elif tokens[0] in WORDS:
				abc_word = tokens[1]
				if tokens[2] == '=':
					pass # use the same dot_word pattern as last time
				else:
					dot_word = tokens[2]
				if tokens[3:]:
					comment = 'For example, in %s' % (', '.join(tokens[3:]))
				else:
					comment = ''

				word = Word(table, dot_word, abc_word, comment)
				for dot in split_dot_word(dot_word):
					dot_letters[dot].things[tokens[0]].append(word)
			else:
				logging.warn('Unknown token %r', tokens)

	pprint(dot_letters[sys.argv[1]].__dict__)

def split_dot_word(dot_word):
	return dot_word.split('-')

def main():
	logging.getLogger().setLevel(logging.INFO)
	parse_table(TABLE)

if __name__=='__main__':
	main()
