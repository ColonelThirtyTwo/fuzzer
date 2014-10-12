
import time
import requests
import logging
logger = logging.getLogger("tester")

from crawler import remove_fragment
from urllib.parse import urljoin

VULNERABILITY = 35 # Log level for vulnerabilities
logging.addLevelName(VULNERABILITY, "VULNERABILITY")

class Tester:
	"""
	Class for testing pages for vulnerabilities
	"""
	
	def __init__(self, crawler, sensitive_data, test_vectors, slow_time, random):
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
		self.vectors = test_vectors
		self.slow_time = slow_time / 1000.0
		
		self.s = crawler.s
	
	def log_vuln(self, page, input_name, vector, logstr, *args):
		logger.log(VULNERABILITY, "%s : %s : %s : "+logstr, page.url, input_name, ("Vector string '"+vector+"'") if vector else "No vector", *args)
	
	def run(self):
		"""
		Runs all tests.
		"""
		for page in self.crawler.pages.values():
			if not page.valid:
				# Skip pages that couldn't be fetched
				continue
			
			logger.info("Fuzzing URL %s", page.url)
			for form in page.forms:
				logger.debug("Fuzzing form %s (%s)", form.action, form.method)
				self.fuzz_form(page, form)
			
			for param in page.get_parameters:
				logger.debug("Fuzzing GET %s", param)
				self.fuzz_get(page, param)
			
			for cookie in self.crawler.cookies:
				logger.debug("Fuzzing cookie %s", cookie)
				self.fuzz_cookie(page, cookie)
		
	def generate_form_data(self, form):
		"""
		Returns a generator that yields three values.
		
		The first is the generated junk, as a dictionary suitable for using as post data.
		The second is the name of the field being replaced with an attack vector, or None if no field
		    is being replaced.
		The third is the attack vector, or None.
		"""
		placeholder_values = {}
		for i in form.fields:
			placeholder_values[i.name] = i.get_placeholder()
		
		yield placeholder_values, None, None
		
		for k in placeholder_values:
			for v in self.vectors:
				nx = placeholder_values.copy()
				nx[k] = v
				yield nx, k, v
	
	def fuzz_form(self, page, form):
		"""
		Fuzzes one form on a page
		"""
		form_name = "Form %s (%s)" % (form.action, form.method)
		form_url = remove_fragment(urljoin(page.url, form.action))
		if form.method.lower() == "post":
			form_method = "POST"
		else:
			form_method = "GET"
		
		for data, k, v in self.generate_form_data(form):
			if not v:
				logger.debug("Fuzzing: No attack vector")
			else:
				logger.debug("Fuzzing: Field '%s' set to vector '%s'", k, v)
			
			if form_method == "POST":
				r = requests.Request(form_method, form_url, data=data)
			else:
				r = requests.Request(form_method, form_url, params=data)
			
			r = self.s.prepare_request(r)
			
			vuln = self.fuzz_one(r, v)
			for msg in vuln:
				self.log_vuln(page, form_name, v, *msg)
	
	def fuzz_get(self, page, param):
		"""
		Fuzzes a GET parameter.
		"""
		get_name = "GET %s" % (param,)
		for v in self.vectors:
			logger.debug("Fuzzing: GET parameter '%s' set to vector '%s'", param, v)
			
			r = requests.Request("GET", page.url, params={param: v})
			r = self.s.prepare_request(r)
			vuln = self.fuzz_one(r, v)
			for msg in vuln:
				self.log_vuln(page, get_name, v, *msg)
	
	def fuzz_cookie(self, page, cookie):
		"""
		Fuzzes a cookie.
		"""
		cookie_name = "Cookie %s" % (cookie,)
		for v in self.vectors:
			logger.debug("Fuzzing: Cookie '%s' set to vector '%s'", cookie, v)
			
			r = requests.Request("GET", page.url, cookies={cookie: v})
			r = self.s.prepare_request(r)
			vuln = self.fuzz_one(r, v)
			for msg in vuln:
				self.log_vuln(page, cookie_name, v, *msg)
	
	def fuzz_one(self, request, vector):
		"""
		Runs one test, and checks for vulnerabilities.
		Returns a list of vulnerability tuples.
		"""
		vulnerabilities = []
		
		start_time = time.monotonic()
		try:
			response = self.s.send(request, timeout=self.slow_time*2, allow_redirects=False)
		except requests.exceptions.Timeout:
			vulnerabilities.append(("Timed out.",))
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
		
		if vector and vector in response.text:
			vulnerabilities.append(("Test vector found unescaped '%s'", vector))
		
		return vulnerabilities
