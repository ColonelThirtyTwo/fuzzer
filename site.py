
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
		self.pages = set()
		self.pagesQueue = [baseurl]
