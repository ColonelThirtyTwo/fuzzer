
from html.parser import HTMLParser
import itertools

class FormField:
	def __init__(self, name):
		self.name = name
	
	def get_values(self):
		"""
		Returns a list of possible values to use.
		"""
		raise NotImplementedError()

class SelectField(FormField):
	"""
	Field for drop-down select and radio types.
	"""
	def __init__(self, name):
		super().__init__(name)
		self.options = [] # list of values
	
	def get_values(self):
		return self.options
	
	def __str__(self):
		return "Select Field: " + str(self.options)

class CheckboxField(FormField):
	def __init__(self, name):
		super().__init__(name)
		self.options = [] # list of values
	
	def get_values(self):
		#for o in intertools.permutations(self.options):
		#	yield ",".join(o) # TODO: is this correct?
		return [self.options[0]]
	
	def __str__(self):
		return "Checkbox Field: " + str(self.options)

class TextField(FormField):
	def __init__(self, name):
		super().__init__(name)
	
	def __str__(self):
		return "Text Field"

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
		if tag == "form":
			self.handle_form_end()
		elif tag == "select":
			self.handle_select_end()
	
	###################################################################
	
	def handle_form_start(self, attrs):
		f = Form(attrs.get("action", "."), attrs.get("method", "GET"))
		self.forms.append(f)
		self.current_form = f
		
	def handle_form_end(self):
		self.current_form = None
	
	def handle_select_start(self, attrs):
		s = SelectField(attrs.get("name","(no name)"))
		self.add_field_to_form(s)
		self.current_field = s
		
	def handle_select_end(self):
		self.current_field = None

	def handle_option(self, attrs):
		if self.current_field:
			self.current_field.options.append(attrs.get("value", "")) # TODO: support default value properly
		
	def handle_input(self, attrs):
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
		else:
			f = TextField(name)
			f.real_type = typ
			self.add_field_to_form(f)
	
	def handle_link(self, attrs):
		l = attrs.get("href","")
		if l:
			self.links.append(l)
	
	def handle_button(self,attrs):
		#b = Button(attrs.get("name",""), attrs)
		#self.add_field_to_form(b)
		pass
	
	def handle_textarea(self,attrs):
		self.add_field_to_form(TextField(attrs.get("name","(no name)")))
	
	def add_field_to_form(self, field):
		self.current_form.fields.append(field)


# parser = DiscovererParser()
# parser.feed('<form><input some="a" some2="b">Test</input>'
            # '<input>Test2</input></form><form>'
			  # '<select><option label="testa"/><option label="testb"/>'
			  # '</select><select></select></form><form></form>')
# parser.close()
# for f in parser.forms:
	# print(f.to_string())