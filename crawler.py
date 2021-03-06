
from urllib.parse import urlparse, urljoin, urlunparse, parse_qs
import requests
import re
from collections import OrderedDict
import logging
logger = logging.getLogger("crawler")

from fuzzparser import DiscovererParser, Form, FormField
import guess

def remove_fragment(url):
	"""
	Strips fragments from the URL
	"""
	if isinstance(url, str):
		url = urlparse(url)
	return urlunparse((url.scheme, url.netloc, url.path, "", "", ""))

class Page:
	"""
	Holds information about a page.
	"""
	
	def __init__(self, url, guessed=False):
		self.url = url
		self.fetched = False
		self.valid = True
		self.guessed = guessed
		
		self.get_parameters = set()
		self.forms = []
	
	def fetch_and_parse(self, site):
		logger.debug("Fetching %s", self.url)
		
		r = site.s.get(self.url)
		self.fetched = True
		
		if r.status_code != requests.codes.ok:
			self.valid = False
			self.response_code = r.status_code
			
			if self.guessed:
				logger.debug("Failed to get guessed page: %s (status code: %d)", self.url, r.status_code)
			else:
				logger.warning("Failed to get page: %s (status code: %d)", self.url, r.status_code)
			
			return
		
		if not r.headers.get("content-type", "").startswith("text/html"):
			logger.info("Skipping %s : Non HTML mime type of %s", self.url, r.headers.get("content-type", "(unknown)"))
			return
		
		site.update_cookies_from_request(r)
		
		parser = DiscovererParser()
		parser.feed(r.text)
		parser.close()
		
		logger.info("Feched %s. Found %d links and %d forms.", self.url, len(parser.links), len(parser.forms))
		
		self.forms = parser.forms
		for rurl in parser.links:
			url = urljoin(self.url, rurl)
			url = remove_fragment(url)
			site.add_page_to_queue(url)
		
		for rurl in site.words_list:
			for ext in guess.EXTENSIONS:
				url = urljoin(self.url, rurl+ext)
				url = remove_fragment(url)
				site.add_page_to_queue(url, guessed=True)
	
	def __hash__(self):
		return hash(self.url)
	
	def __eq__(self, other):
		return self.url == other.url

class Site:
	"""
	Holds information about a site, including entries for its pages.
	"""
	
	def __init__(self, wordslist, blacklist=None):
		self.pages = OrderedDict()
		self.pages_queue = []
		self.cookies = set()
		self.words_list = wordslist
		self.blacklist = blacklist or []
	
	def crawl(self, url, auth=None, cookies=None):
		"""
		Begins crawling from a URL.
		
		The URL should be absolute. Pages in other sites will not be crawled.
		
		If auth is supplied, it should be a dictionary of POST parameters. Instead of starting at url, the
		crawler will first send a POST request to the url with the passed parameters, then start crawling at
		wherever it was redirected to.
		"""
		self.s = requests.Session()
		
		if not urlparse(url).scheme:
			url = "http://"+url
		
		if auth is not None:
			
			r = self.s.post(url, data=auth, allow_redirects=False, cookies=cookies)
			if "Location" in r.headers:
				url = urljoin(url, r.headers["Location"])
				url = remove_fragment(url)
				logger.info("Authenticated and redirected to %s", url)
			else:
				logger.warning("Login page didn't redirect anywhere. Check the authentication data.")
		
		self.site = urlparse(url).netloc
		self.add_page_to_queue(url)
		
		while self.pages_queue:
			self.crawl_one()
	
	def crawl_one(self):
		page = self.pages_queue.pop(0)
		page.fetch_and_parse(self)
	
	def add_page_to_queue(self, url, guessed=False):
		"""
		Adds a URL to the page queue, and parses for GET parameters.
		
		The URL should be absolute.
		
		If the URL has already been parsed or is already in the queue, updates the
		applicable GET parameters but otherwise does nothing.
		
		If the URL is not from this site or is not http, ignores it.
		"""
		o = urlparse(url)
		
		# Check if not HTTP or in other site
		if o.scheme != "http" or o.netloc != self.site:
			return
		
		# Check blacklist
		if o.path in self.blacklist:
			return
		
		# Get canonical URL (without get parameters/fragments) and get or create a page
		canonical_url = urlunparse(("http", o.netloc, o.path, "", "", ""))
		if canonical_url in self.pages:
			p = self.pages[canonical_url]
			if not guessed:
				# Possibly crawled a page that was guessed earlier.
				p.guessed = False
		else:
			p = Page(canonical_url, guessed)
			self.pages[canonical_url] = p
			self.pages_queue.append(p)
			logger.debug("Added %s to queue", canonical_url)
		
		# Update possible GET paremeters
		get_params = parse_qs(o.query)
		p.get_parameters.update(get_params.keys())
	
	def update_cookies_from_request(self, r):
		"""
		Adds cookies from r to the list of cookie names for the site.
		"""
		self.cookies.update(r.cookies.keys())
