import logging
from collections import defaultdict, namedtuple
from pprint import pprint

import sys
import os

# http://liblouis.org/documentation/liblouis.html

# apt-get install liblouis-data
TABLE_DIR='/usr/share/liblouis/tables/'

Word = namedtuple('Word', 'table pattern abc_word comment')

WORDS = {'always', 'begword', 'word', 'midendword', 'joinword', 'sufword', 'lowword', 'midword', 'endword', 'endnum', 'largesign', 'begnum', 'sign', 'litdigit', 'joinnum', 'midnum', 'uplow', 'prepunc', 'postpunc', 'decpoint', 'multind', 'letter', 'hyphen', 'punctuation'}

FORMATTING = {'begital', 'endital', 'begbold', 'endbold', 'begcaps', 'endcaps', 'capsign', 'numsign', 'letsign', 'begcomp', 'endcomp'}

IGNORE = {'literal', 'include', 'repeated', 'contraction'}

class DotLetter(object):
	def __init__(self):
		self.things = {w : defaultdict(list) for w in WORDS | FORMATTING}
	def __repr__(self):
		return 'DotLetter(%r)' % (self.__dict__,)
	def pretty(self):
		return '\n\n'.join(
			'%s:\n%s' % (
				section,
				'\n'.join(
					'\t%s =>\n%s' % (
						dotword,
						'\n'.join(
							'\t\t%s: %r' % (
								word.abc_word,
								word)
							for word in words))
						for dotword, words in dot_word_list.items()))
				for section, dot_word_list in self.things.items())

def parse_tables(tabledir):
	dot_letters = defaultdict(DotLetter)

	for end in os.listdir(tabledir):
		table = os.path.join(tabledir, end)
		logging.info('Parsing table %r', table)
		with open(table) as f:
			parse_table(dot_letters, f, table)

	print dot_letters[sys.argv[1]].pretty()

def parse_table(dot_letters, f, table):
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
				dot_letters[dot].things[tokens[0]][dot_word].append(word)

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
				dot_letters[dot].things[tokens[0]][dot_word].append(word)
		else:
			logging.warn('Unknown token %r', tokens)

def split_dot_word(dot_word):
	return dot_word.split('-')

def main():
	logging.getLogger().setLevel(logging.INFO)
	parse_tables(TABLE_DIR)

if __name__=='__main__':
	main()
