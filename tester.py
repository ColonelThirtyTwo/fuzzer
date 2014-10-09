
import time
import requests
import logging
logger = logging.getLogger("tester")

VULNERABILITY = 35 # Log level for vulnerabilities
logging.addLevel(VULNERABILITY, "VULNERABILITY")

class FormJunkGenerator:
	"""
	Class for generating junk data for forms.
	Takes into account each field's type.
	"""
	
	def __init__(self, form):
		self.form = form
	
	def _get_data(self, fields, cur_field):
		pass
	
	def generate(self):
		"""
		Returns a generator that yields the generated junk, as a dictionary suitable for using
		as post data.
		"""
		yield from self._get_data()

class Tester:
	"""
	Class for testing pages for vulnerabilities
	"""
	
	def __init__(self, crawler, sensitive_data, test_vectors, slow_time):
		"""
		Creates the Tester.
		
		crawler should be a completed Crawler class; that is, it has already ran and crawled the site.
		sensitive_data is a list or set of strings that should never appear in a response.
		test_vectors is a list or set of strings to use as test input.
		slow_time is a duration (in milliseconds) after which a response is considered 'slow'. The request timeout is set to
		double this amount.
		"""
		self.crawler = crawler
		self.sensitive_data = sensitive_data
		self.test_vectors = test_vectors
		self.slow_time = slow_time / 1000.0
		
		self.s = crawler.s
	
	def log_vuln(self, page, input_name, vector, logstr, *args):
		logger.log(VULNERABILITY, "%s : %s : Vector string '%s' : "+logstr, page.url, input_name, vector, *args)
	
	def test_page(self, page):
		"""
		Tests all inputs on one page.
		"""
		pass
	
	def run_test(self, page, input_name, request, vectors):
		"""
		Runs one test, and checks for vulnerabilities.
		Returns a list of vulnerability tuples.
		"""
		vulnerabilities = []
		
		start_time = time.monotonic()
		try:
			response = self.s.send(request, timeout=self.slow_time*2)
		except requests.exceptions.Timeout:
			vulnerabilities.append(("Timed out."))
			return vulnerabilities
		end_time = time.monotonic()
		
		if end_time - start_time >= self.slow_time:
			vulnerabilities.append(("Slow response (%f seconds)", end_time-start_time))
		
		if response.status_code != 200:
			vulnerabilities.append(("Got status code %s", response.status_code))
			return vulnerabilities
		
		for s in self.sensitive_data:
			if s in response.text:
				vulnerabilities.append(("Sensitive data found '%s'", s))
		
		for vector in vectors:
			if vector in response.text:
				vulnerabilities.append(("Test vector found unescaped '%s'", vector))
		
		return vulnerabilities
