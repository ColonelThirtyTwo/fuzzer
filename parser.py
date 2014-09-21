
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
		
class Select(FormField):
	def __init__(self, name):
		super().__init__(name, "select")
		self.options = []

class Option:
	def __init__(self, label, selected, value):
		self.label = label
		self.selected = selected
		self.value = value

class Button:
	def __init__(self, name, type, value):
		self.name = name
		self.type = type
		self.value = value

class DiscovererParser(HTMLParser):
	
	def __init__(self):
		super().__init__()
		self.forms = []
		self.current_form = None
		self.links = []
		self.fields = []
	
	def handle_starttag(self, tag, attrs_list):
		attrs = dict()
		for key, value in attrs_list:
			attrs[key] = value
		
		if tag == "form":
			self.handle_form_start(attrs)
		elif tag == "a":
			self.handle_link(attrs)
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
	
	# #################################################################
	
	def handle_form_start(self, attrs):
		f = Form(attrs.get("action", "."), attrs.get("method", "GET"))
		self.forms.append(f)
		self.current_form = f
		
	def handle_form_end(self, attrs):
		self.current_form = None
	
	def handle_select_start(self, attrs):
		s = Select(attrs.get("name",""))
		self.add_field_to_form(s)
		self.current_form = s
		
	def handle_select_end(self,attrs):
		self.current_select = None

	def handle_option(self,attrs):
		o = Option(attrs.get("label",""),attrs.get("selected","false"),attrs.get("value",""))
		if self.current_select:
			self.current_select.options.append(o)
		
	def handle_input(self, attrs):
		field = FormField(attrs.get("name", ""), attrs.get("type", "text"))
		self.add_field_to_form(field)
	
	def handle_link(self, attrs):
		l = attrs.get("href","")
		if len(l) > 0:
			self.links.append(l)
	
	def handle_button(self,attrs):
		b = Button(attrs.get("name",""), attrs.get("type",""), attrs.get("value",""))
		self.add_field_to_form(b)
	
	def handle_textarea(self,attrs):
		#todo
		return
	
	def add_field_to_form(self, field):
		if not self.current_form:
			self.fields.append(field)
		else:
			self.current_form.fields.append(field)
	