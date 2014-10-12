
import sys
import argparse
import json
import logging
logging.basicConfig(format="%(levelname)10s:%(message)s", level=logging.WARNING, stream=sys.stderr)
#logging.basicConfig(level=logging.DEBUG, stream=sys.stderr)

from crawler import Site
from tester import Tester

def parse_args():
	parser = argparse.ArgumentParser()
	subparsers = parser.add_subparsers(title="Subcommands", dest="command")
	
	discover_parser = subparsers.add_parser("discover",help="Crawls a site, discovering its inputs")
	test_parser = subparsers.add_parser("test", help="Crawls a site and fuzzes each input")
	
	parser.add_argument("--custom-auth", dest="customauth", help="Custom authentication string. This should be a JSON-encoded string of POST parameters to pass to the first URL.", default=None)
	parser.add_argument("--cookies", help="Custom cookies string. This should be a JSON-encoded string of cookies to set before fuzzing but after logging in. Requires --custom-auth", default=None)
	parser.add_argument("-b", "--blacklist", help="Blacklists a certain URL. Should be an absolute path with a leading slash. This argument can be specified multiple times.", action="append")
	
	log_levels = parser.add_mutually_exclusive_group()
	log_levels.add_argument("-v", "--verbose", action="store_true", dest="verbose", help="Output verbose debugging info", default=False)
	log_levels.add_argument("-q", "--quiet", action="store_true", dest="quiet", help="Do not output anything except errors and results", default=False)
	
	discover_parser.add_argument("url", help="URL to start crawling at")
	discover_parser.add_argument("--common-words", metavar="words.txt", dest="commonwords", required=True, help="File of common words to use in input and URL guessing", type=argparse.FileType())
	
	test_parser.add_argument("url", help="URL to start crawling at")
	test_parser.add_argument("-v", "--vectors", metavar="vectors.txt", help="Filename of newline-separated test vectors.", required=True, type=argparse.FileType())
	test_parser.add_argument("-s", "--sensitive", metavar="sensitive.txt", help="Filename of newline-separated data that should be considered sensitive and should never appear in a page.", type=argparse.FileType(), required=True)
	test_parser.add_argument("-l", "--slow", metavar="ms", help="Number of milliseconds before the response is considered to be slow.", type=int, default=500)
	test_parser.add_argument("-r", "--random", dest="random", help="Fuzz pages and inputs in a random order rather than sequentially.", action="store_true")
	
	args = parser.parse_args()
	if "command" not in vars(args) or not args.command:
		parser.print_help()
		sys.exit(1)
	return args

def cmd_discover(args, auth, cookies):
	words = list()
	for word in args.commonwords:
		word = word.strip()
		if word:
			words.append(word)
	args.commonwords.close()
	
	crawler = Site(words, args.blacklist)
	crawler.crawl(args.url, auth, cookies)
	
	for page in crawler.pages.values():
		# Warn if page wasn't retreived successfully, but only if it wasn't guessed.
		if not page.valid:
			if not page.guessed:
				print("Couldn't fetch", page.url, "(status code:", page.response_code, ")")
			continue
		
		print(page.url)
		
		if page.guessed:
			print("\t Page URL was guessed.")
		
		print("\t", len(page.forms), "form(s)")
		for form in page.forms:
			print("\t\t", form.action, form.method)
			
			for field in form.fields:
				print("\t\t\t", field.name, " : ", str(field))
		
		print("\t", len(page.get_parameters), "GET parameter(s)")
		for param in page.get_parameters:
			print("\t\t", param)

def cmd_test(args, auth, cookies):
	sensitive_data, vectors = [], []
	for sensitive in args.sensitive:
		sensitive = sensitive.strip()
		if sensitive:
			sensitive_data.append(sensitive)
	args.sensitive.close()
	
	for v in args.vectors:
		v = v.strip()
		if v:
			vectors.append(v)
	args.vectors.close()
	
	crawler = Site([], args.blacklist)
	crawler.crawl(args.url, auth, cookies)
	
	fuzzer = Tester(crawler, sensitive_data, vectors, args.slow, args.random)
	if args.random:
		fuzzer.run_random()
	else:
		fuzzer.run()

########################################################################

if __name__ == "__main__":
	args = parse_args()
	
	if args.verbose:
		logging.getLogger("crawler").setLevel(logging.DEBUG)
		logging.getLogger("tester").setLevel(logging.DEBUG)
	elif args.quiet:
		logging.getLogger("crawler").setLevel(logging.ERROR)
		logging.getLogger("tester").setLevel(logging.ERROR)
	else:
		logging.getLogger("crawler").setLevel(logging.INFO)
		logging.getLogger("tester").setLevel(logging.INFO)
	
	if args.customauth:
		try:
			auth = json.loads(args.customauth)
		except ValueError as e:
			print("Invalid custom-auth string:")
			print(str(e))
			sys.exit(1)
	else:
		auth = None
	
	if args.cookies:
		try:
			cookies = json.loads(args.cookies)
		except ValueError as e:
			print("Invalid cookies string:")
			print(str(e))
			sys.exit(1)
	else:
		cookies = None
	
	if args.command == "test":
		cmd_test(args, auth, cookies)
	elif args.command == "discover":
		cmd_discover(args, auth, cookies)
