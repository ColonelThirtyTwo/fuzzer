
from urllib.parse import urlparse, parse_qs

class Page:
	"""
	Holds information about a page.
	"""
	
	def __init__(self, url):
		self.url = url
		self.get_parameters = set()
		self.form_parameters = set()
		self.cookies = set()
	
	def fetch_and_parse(self):
		pass
	
	def __hash__(self):
		return hash(self.url)
	
	def __eq__(self, other):
		return self.url == other.url

class Site:
	"""
	Holds information about a site, including entries for its pages.
	"""
	
	def __init__(self, baseurl):
		self.url = baseurl
		self.pages = dict()
		self.pagesQueue = []
	
	def crawl(url, auth=None):
		pass
	
	def add_page_to_queue(url):
		"""
		Adds a URL to the page queue, and parses for GET parameters.
		
		The URL should be absolute.
		
		If the URL has already been parsed or is already in the queue, updates the
		applicable GET parameters but otherwise does nothing.
		
		If the URL is not from this site or is not http, ignores it.
		"""
		o = urlparse(url)
		
		if o.scheme != "http":
			return
		
		# TODO: Check for same site
		
		canonical_url = o.netloc + o.path
		if canonical_url in self.pages:
			p = self.pages[canonical_url]
		else:
			p = Page(canonical_url)
			self.pages[canonical_url] = p
			self.pagesQueue.append(p)
			print("Added", canonical_url, "to queue")
		
		get_params = parse_qs(o.query)
		p.get_parameters.update(get_params.keys())
