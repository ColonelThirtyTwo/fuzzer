
from html.parser import HTMLParser

class FormField:
	def __init__(self, name, typ):
		self.name = name
		self.type = typ

class Form:
	def __init__(self, action, method):
		self.action = action
		self.method = method
		self.fields = []

class DiscovererParser(HTMLParser):
	
	def __init__(self):
		super().__init__()
		self.forms = []
		self.current_form = None
		self.links = []
	
	def handle_starttag(self, tag, attrs):
		if tag == "form":
			self.handle_form_start(attrs)
		elif current_form and tag == "input":
			self.handle_form_input(tag, attrs)
		elif tag == "a":
			self.handle_link(self, attrs)
		elif tag == "input":
			return
	
	def handle_endtag(self, tag):
		if tag == "form":
			self.handle_form_end()
	
	# #################################################################
	
	def handle_form_start(self, attrs):
		f = Form(attrs.get("action", "."), attrs.get("method", "GET"))
		self.forms.append(f)
		self.current_form = f
	
	def handle_form_input(self, tag, attrs):
		field = FormField(attrs.get("name", ""), attrs.get("type", "text"))
		self.current_form.fields.append(field)
	
	def handle_form_end(self, attrs):
		self.current_form = None
	
	def handle_link(self, attrs):
		l = attrs.get("href","")
		if len(l) > 0:
			self.links.append(l)
	