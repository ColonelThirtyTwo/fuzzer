
from html.parser import HTMLParser
import itertools

class FormField:
	def __init__(self, name):
		self.name = name
	
	def get_placeholder(self):
		"""
		Returns a value that can be used in the form when not testing this input for
		XSS.
		"""
		raise NotImplementedError()

class SelectField(FormField):
	"""
	Field for drop-down select and radio types.
	"""
	def __init__(self, name):
		super().__init__(name)
		self.options = [] # list of values
	
	def get_placeholder(self):
		return self.options[0]
	
	def __str__(self):
		return "Select Field: " + str(self.options)

class CheckboxField(FormField):
	def __init__(self, name):
		super().__init__(name)
		self.options = [] # list of values
	
	def get_placeholder(self):
		return None
	
	def __str__(self):
		return "Checkbox Field: " + str(self.options)

class TextField(FormField):
	def __init__(self, name):
		super().__init__(name)
	
	def get_placeholder(self):
		return ""
	
	def __str__(self):
		return "Text Field"

class ButtonField(FormField):
	def __init__(self, name, value):
		super().__init__(name)
		self.value = value
	
	def get_placeholder(self):
		return self.value
	
	def __str__(self):
		return "Button"

class Form:
	def __init__(self, action, method):
		self.action = action
		self.method = method
		self.fields = []
	
	def to_string(self):
		s = "Form action:" + self.action + " method:" + self.method + " fields:"
		s += "None\n" if len(self.fields) == 0 else "\n"
		for f in self.fields:
			s += "\t" + str(f) + "\n"
		return s

class DiscovererParser(HTMLParser):
	
	def __init__(self):
		super().__init__()
		self.forms = []
		self.current_form = None
		self.current_select = None
		self.current_field = None
		self.links = []
	
	def handle_starttag(self, tag, attrs_list):
		"""
		Handles parsing of html start tag
		"""
		attrs = dict()
		for key, value in attrs_list:
			attrs[key] = value
		
		if tag == "form":
			self.handle_form_start(attrs)
		elif tag == "a":
			self.handle_link(attrs)
		elif not self.current_form:
			return # Don't process form fields without a current form.
		elif tag == "input":
			self.handle_input(attrs)
		elif tag == "select":
			self.handle_select_start(attrs)
		elif tag == "option":
			self.handle_option(attrs)
		elif tag == "button":
			self.handle_button(attrs)
		elif tag == "textarea":
			self.handle_textarea(attrs)
		
	def handle_endtag(self, tag):
		"""
		Handles parsing of html end tag
		"""
		if tag == "form":
			self.handle_form_end()
		elif tag == "select":
			self.handle_select_end()
	
	###################################################################
	
	def handle_form_start(self, attrs):
		"""
		Handles parsing of the start of a form
		"""
		f = Form(attrs.get("action", "."), attrs.get("method", "GET"))
		self.forms.append(f)
		self.current_form = f
		
	def handle_form_end(self):
		"""
		Handles parsing of end of a form
		"""
		self.current_form = None
	
	def handle_select_start(self, attrs):
		"""
		Handles parsing of the start of a select
		"""
		s = SelectField(attrs.get("name","(no name)"))
		self.add_field_to_form(s)
		self.current_field = s
		
	def handle_select_end(self):
		"""
		Handles parsing of end of a select
		"""
		self.current_field = None

	def handle_option(self, attrs):
		"""
		Handles parsing of of options
		"""
		if self.current_field:
			self.current_field.options.append(attrs.get("value", "")) # TODO: support default value properly
		
	def handle_input(self, attrs):
		"""
		Handles parsing of input
		"""
		typ = attrs.get("type", "text")
		name = attrs.get("name", "(no name)")
		
		if typ in ("text", "url", "email"):
			self.add_field_to_form(TextField(name))
		elif typ == "radio":
			if name in self.current_form.fields:
				self.current_form.fields[name].options.append(attrs.get("value", ""))
			else:
				f = SelectField(name)
				f.options.append(attrs.get("value", ""))
				self.add_field_to_form(f)
		elif typ == "checkbox":
			if name in self.current_form.fields:
				self.current_form.fields[name].options.append(attrs.get("value", ""))
			else:
				f = CheckboxField(name)
				f.options.append(attrs.get("value", ""))
				self.add_field_to_form(f)
		elif typ == "submit":
			self.add_field_to_form(ButtonField(name, attrs.get("value", "")))
		else:
			f = TextField(name)
			f.real_type = typ
			self.add_field_to_form(f)
	
	def handle_link(self, attrs):
		"""
		Handles parsing of links
		"""
		l = attrs.get("href","")
		if l:
			self.links.append(l)
	
	def handle_button(self,attrs):
		"""
		Handles parsing of buttons
		"""
		#b = Button(attrs.get("name",""), attrs)
		#self.add_field_to_form(b)
		pass
	
	def handle_textarea(self,attrs):
		"""
		Handles parsing of textarea
		"""
		self.add_field_to_form(TextField(attrs.get("name","(no name)")))
	
	def add_field_to_form(self, field):
		"""
		Helper function that adds a field to the classes current form.
		"""
		self.current_form.fields.append(field)
