
from urllib.parse import urlparse, urljoin, urlunparse, parse_qs
import requests

from parser import DiscovererParser, Form, FormField
import guess

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
		self.forms = None
	
	def fetch_and_parse(self, site):
		r = site.s.get(self.url)
		
		if r.status_code != requests.codes.ok:
			self.valid = False
			self.response_code = r.status_code
			return
		
		site.update_cookies_from_request(r)
		
		parser = DiscovererParser()
		parser.feed(r.content)
		parser.close()
		
		self.forms = parser.forms
		for rurl in parser.links:
			url = urljoin(self.url, rurl, allow_fragments=False)
			site.add_page_to_queue(url)
		
		for rurl in guess.iter():
			url = urljoin(self.url, rurl, allow_fragments=False)
			site.add_page_to_queue(url, guessed=True)
		
		self.fetched = True
	
	def __hash__(self):
		return hash(self.url)
	
	def __eq__(self, other):
		return self.url == other.url

class Site:
	"""
	Holds information about a site, including entries for its pages.
	"""
	
	def __init__(self):
		self.pages = dict()
		self.pagesQueue = []
		self.cookies = set()
	
	def crawl(self, url, auth=None):
		"""
		Begins crawling from a URL.
		
		The URL should be absolute. Pages in other sites will not be crawled.
		
		If auth is supplied, it should be a dictionary of POST parameters. Instead of starting at url, the
		crawler will first send a POST request to the url with the passed parameters, then start crawling at
		wherever it was redirected to.
		"""
		self.s = requests.Session()
		
		if auth is not None:
			r = s.post(url, data=auth, allow_redirects=False)
			if "Location" in r.headers:
				url = r.headers["Location"]
		
		self.site = urlparse(url).netloc
		self.add_page_to_queue(url)
		
		while self.pagesQueue:
			pass
	
	def crawl_one(self):
		page = self.pagesQueue.pop(0)
		page.fetch_and_parse(self.s)
	
	def add_page_to_queue(url, guessed=False):
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
		
		# Get canonical URL (without get parameters/fragments) and get or create a page
		canonical_url = urlunparse(("http", o.netloc, o.path, "", "", ""))
		if canonical_url in self.pages:
			p = self.pages[canonical_url]
		else:
			p = Page(canonical_url, guessed)
			self.pages[canonical_url] = p
			self.pagesQueue.append(p)
			print("Added", canonical_url, "to queue")
		
		# Update possible GET paremeters
		get_params = parse_qs(o.query)
		p.get_parameters.update(get_params.keys())
	
	def update_cookies_from_request(self, r):
		"""
		Adds cookies from r to the list of cookie names for the site.
		"""
		self.cookies.update(r.cookies.keys())
