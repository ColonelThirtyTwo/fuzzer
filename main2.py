
import sys
import argparse
import json
import logging
logging.basicConfig(format="%(levelname)10s:%(message)s", level=logging.WARNING, stream=sys.stderr)

from crawler import Site

def parse_args():
	parser = argparse.ArgumentParser()
	subparsers = parser.add_subparsers(title="Subcommands", dest="command")
	
	discover_parser = subparsers.add_parser("discover",help="Discovers inputs to the website")
	test_parser = subparsers.add_parser("test", help="Not implemented yet")
	
	parser.add_argument("--custom-auth", dest="customauth", help="Custom authentication string. This should be a JSON-encoded string of POST parameters to pass to the first URL.", default=None)
	
	log_levels = parser.add_mutually_exclusive_group()
	log_levels.add_argument("-v", "--verbose", action="store_true", dest="verbose", help="Enable verbose output", default=False)
	log_levels.add_argument("-q", "--quiet", action="store_true", dest="quiet", help="Do not output anything except errors and results", default=False)
	
	discover_parser.add_argument("url", help="URL to start crawling at")
	discover_parser.add_argument("--common-words", dest="commonwords", required=True, help="File of common words to use in input and URL guessing", type=argparse.FileType())

	args = parser.parse_args()
	if "command" not in vars(args) or not args.command:
		parser.print_help()
		sys.exit(1)
	return args

def cmd_test(args):
	print("test command not supported yet")
	sys.exit(1)

def cmd_discover(args):
	if args.verbose:
		logging.getLogger("crawler").setLevel(logging.DEBUG)
	elif args.quiet:
		logging.getLogger("crawler").setLevel(logging.ERROR)
	else:
		logging.getLogger("crawler").setLevel(logging.INFO)
	
	if args.customauth:
		try:
			auth = json.loads(args.customauth)
		except ValueError as e:
			print("Invalid custom-auth string:")
			print(str(e))
			sys.exit(1)
	else:
		auth = None
	
	words = list()
	for word in args.commonwords:
		words.append(word)
	args.commonwords.close()
	
	crawler = Site(words)
	crawler.crawl(args.url, auth)
	
	for page in crawler.pages.values():
		if not page.valid:
			if not page.guessed:
				print("Couldn't fetch", page.url, "(status code:", page.response_code, ")")
			continue
		
		print(page.url)
		
		if page.guessed:
			print("\t Page URL was guessed.")
		
		print("\t", len(page.forms), "forms")
		for form in page.forms:
			print("\t\t", form.action, form.method)
		
		print("\t", len(page.get_parameters), "GET parameters")
		for param in page.get_parameters:
			print("\t\t", param)

args = parse_args()
if args.command == "test":
	cmd_test(args)
elif args.command == "discover":
	cmd_discover(args)
