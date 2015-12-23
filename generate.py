import logging

import louis_parser

def main():
	logging.getLogger().setLevel(logging.INFO)
	rules = louis_parser.parse_tables(louis_parser.TABLE_DIR)


def print_interesting(interesting, rules):
	by_abc_word = defaultdict(list)
	for rule in rules:
		if rule.dot_word == (interesting,):
			by_abc_word[rule.abc_word].append(rule)
	for k, r in by_abc_word.items():
		print k.encode("utf8")
		print '\t', r

if __name__=='__main__':
	main()
