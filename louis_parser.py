import logging
import sys
import os
import re
from collections import defaultdict, namedtuple
from pprint import pprint

# http://liblouis.org/documentation/liblouis.html

# apt-get install liblouis-data
TABLE_DIR='/usr/share/liblouis/tables/'

class Rule(namedtuple('_Rule', 'table opcode dot_word abc_word comment')):
	@property
	def locale(self):
		return self.table.split('.')[0].lower()


WORDS = {
	'always',
	'begword',
	'word',
	'midendword',
	'joinword',
	'sufword',
	'lowword',
	'midword',
	'endword',
	'endnum',
	'largesign',
	'begnum',
	'sign',
	'litdigit',
	'joinnum',
	'midnum',
	'uplow',
	'prepunc',
	'postpunc',
	'decpoint',
	'multind',
	'letter',
	'hyphen',
	'punctuation',
	'uppercase',
	'lowercase',
	'digit',
	'math',
	'space',
	'display',
	'syllable',
}

FORMATTING = {
	'begital',
	'endital',
	'begbold',
	'endbold',
	'begcaps',
	'endcaps',
	'capsign',
	'numsign',
	'letsign',
	'begcomp',
	'endcomp',
}

IGNORE = {
	'literal',
	'include',
	'repeated',
	'contraction',
	'compbrl',
	'replace',
	'pass1',
	'pass2',
	'pass3',
	'pass4',
	'nocont',
	'noletsign',
	'noletsignafter',
}

def parse_tables(tabledir):
	"""Main function. Call this to get a list of rules.
	"""
	rules = []

	for fileend in os.listdir(tabledir):
		if fileend.endswith(".dic"):
			continue

		fullfilename = os.path.join(tabledir, fileend)
		logging.info('Parsing table %r', fullfilename)
		with open(fullfilename) as f:
			rules.extend(parse_table(f, fileend))

	return rules

def parse_table(f, table):
	for line in f:
		tokens = line.strip().split()

		if not tokens:
			continue

		opcode = tokens[0]

		if opcode.startswith('#'):
			continue

		if opcode in IGNORE:
			continue

		elif opcode in FORMATTING:
			abc_word = tokens[1]
			if tokens[2:]:
				comment = 'For example, in %s' % (', '.join(tokens[2:]))
			else:
				comment = ''
			dot_word = ''
			yield Rule(table, opcode, split_dot_word(dot_word), decode_abc_word(abc_word), comment)

		elif opcode in WORDS:
			abc_word = tokens[1]
			if tokens[2] == '=':
				pass # use the same dot_word pattern as last time
			else:
				dot_word = tokens[2]
			if tokens[3:]:
				comment = 'For example, in %s' % (', '.join(tokens[3:]))
			else:
				comment = ''
			yield Rule(table, opcode, split_dot_word(dot_word), decode_abc_word(abc_word), comment)

		else:
			logging.warn('Unknown token %r', tokens)

def split_dot_word(dot_word):
	return tuple(dot_word.split('-'))

def decode_abc_word(abc_word):
	def replace_abc_word(m):
		return unichr(int(m.group(1), 16))
	return re.sub(r'\\[xXuU]([A-Fa-f0-9]{4})', replace_abc_word, abc_word.decode('utf8', 'replace')) # XXX actually this decoding depends on the file's encoding system (which is described in the filename)

def adjust_uplow(rules):
	""" Rules of opcode='uplow' have abc_word of uppercase and lowecase letters together, eg: 'Aa'
	This splits uplow into 2 rules.
	"""
	out = []
	for rule in rules:
		if rule.opcode == 'uplow':
			upper, lower = rule.abc_word
			if ',' in rule.dot_word:
				upperdot, lowerdot = rule.dot_word.split(',')
			else:
				upperdot = lowerdot = rule.dot_word
			out.append(rule._replace(abc_word=upper, dot_word=upperdot))
			out.append(rule._replace(abc_word=lower, dot_word=lowerdot))
		else:
			out.append(rule)
	return out
