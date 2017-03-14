#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Usage: 
  condict.py <word> [--raw] [--more]
  condict.py (-h | --help)
  condict.py (-v | --version)

Options:
  -h --help        Show this screen.
  -v --version     Show version.
  --raw            Print the raw response.
  --more		   Do more search for the word.
"""
# http://python-future.org/compatible_idioms.html
from __future__ import print_function

import json

from docopt import docopt
import requests

URL = 'http://fanyi.youdao.com/openapi.do?keyfrom=con-dict&'\
	  'key=632926943&type=data&doctype=json&version=1.1&q={}'
YOUDAO_API_KEY = '632926943'
KEY_FROM = 'con-dict'
SITE_NAME = 'con-dict'

# http://stackoverflow.com/a/287944
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def raw(response):
	# http://stackoverflow.com/a/11759156/7699087
	print(json.dumps(response, indent=4, sort_keys=True, ensure_ascii=False))


def pretty(response):
	# translation = response['translation']
	search_text = response['query']
	print(bcolors.WARNING, search_text, bcolors.ENDC)

	try:
		explains = response['basic']['explains']
		for item in explains:
			print('', bcolors.OKBLUE, item, bcolors.ENDC)
		print()
	except:
		pass
	
	try:
		web = response['web']
		for item in web:
			print('', bcolors.OKGREEN, item['key'], bcolors.ENDC, \
				':', ','.join(item['value']))
	except:
		pass

def error(response):
	print(bcolors.FAIL, 'Definition for', '\"' + response['query'] + \
		'\"', 'not found', bcolors.ENDC)
	raw(response)


def condict(word, print_raw=False, more=False):
	url = URL.format(word)
	r = requests.get(url)
	json_str = json.loads(r.text)

	if print_raw:
		raw(json_str)
	else:
		pretty(json_str)


def main():
	args = docopt(__doc__, version='condict')

	kwargs = {
        'word': args['<word>'],
        'print_raw': args['--raw'],
        'more': args['--more']
    }

	condict(**kwargs)


if __name__ == '__main__':
	main()