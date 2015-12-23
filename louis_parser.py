import logging
from collections import defaultdict, namedtuple
from pprint import pprint

TABLE='/usr/share/liblouis/tables/en-GB-g2.ctb'

# http://liblouis.org/documentation/liblouis.html

Pattern = namedtuple('Pattern', 'table word comment')

def parse_table(table):
	dot_words = defaultdict(list)
	with open(table) as f:
		for line in f:
			tokens = line.strip().split()

			if not tokens:
				continue
			if tokens[0].startswith('#'):
				continue

			if tokens[0] == 'always':
				word = tokens[1]
				if tokens[2] == '=':
					pass # use the same dot pattern as last time
				else:
					dot = tokens[2]
				if tokens[3:]:
					comment = 'For example, in %s' % (', '.join(tokens[3:]))
				else:
					comment = ''
				dot_words[dot].append(Pattern(table, word, comment))
			else:
				logging.warn('Unknown token %r', tokens)
	pprint(dict(
		letter_patterns(dot_words)
	))

def letter_patterns(dot_words):
	char_lookup = defaultdict(dict)
	for dot_word, patterns in dot_words.items():
		for dot in dot_word.split('-'):
			char_lookup[dot][dot_word] = patterns
	return char_lookup

def main():
	logging.getLogger().setLevel(logging.INFO)
	parse_table(TABLE)

if __name__=='__main__':
	main()
