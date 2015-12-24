import logging
import operator
import os
from collections import defaultdict, namedtuple
from jinja2 import Environment, FileSystemLoader

import louis_parser

OUT_DIR = './out/'

AbcRules = namedtuple('AbcRules', 'abc rules')

def main():
	logging.getLogger().setLevel(logging.INFO)
	rules = louis_parser.parse_tables(louis_parser.TABLE_DIR)
	rules = louis_parser.adjust_uplow(rules)

	rules_by_dot_word = group_by_dot_word(rules)

	for dot_word, specific_rules in rules_by_dot_word.items():
		if len(dot_word) == 1:
			print_interesting(dot_word, specific_rules)


def group_by_dot_word(rules):
	rules_for_dot_word = {}
	for rule in rules:
		rules_for_dot_word.setdefault(rule.dot_word, []).append(rule)
	return rules_for_dot_word

def group_by_abc_word(rules_for_dot_word):
	by_abc_word_dict = defaultdict(list)
	for rule in rules_for_dot_word:
		by_abc_word_dict[rule.abc_word].append(rule)

	by_abc_word = []
	for abc, rules in sorted(by_abc_word_dict.items(), key=lambda (k, rule_list) : (len(rule_list), k), reverse=True): # most common cases first
		rules.sort(key=operator.attrgetter('table'))
		by_abc_word.append(AbcRules(abc, rules))

	return by_abc_word

def print_interesting(dot_word, rules_by_dot_word):
	logging.info("Generating %s", dot_word)

	by_abc_word = group_by_abc_word(rules_by_dot_word)

	env = Environment(loader=FileSystemLoader('./templates/'))
	template = env.get_template('dot.html')

	joined_dot_word = '-'.join(dot_word)

	out_filename = os.path.join(OUT_DIR, '%s.html' % (joined_dot_word,))
	with open(out_filename, 'w') as f:
		f.write(template.render(dot_word=joined_dot_word, rules_by_abc=by_abc_word).encode('utf8'))

if __name__=='__main__':
	main()
