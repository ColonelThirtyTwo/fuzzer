
from html.parser import HTMLParser

class FormField:
	def __init__(self, name, typ, attrs):
		self.name = name
		self.type = typ
		self.attrs = attrs
	def to_string(self):
		return "input type:" + self.type + " attributes: " + str(self.attrs)
		
	
class Form:
	def __init__(self, action, method):
		self.action = action
		self.method = method
		self.fields = []
	def to_string(self):
		s = "Form action:" + self.action + " method:" + self.method + " fields:"
		s += "None\n" if len(self.fields) == 0 else "\n"
		for f in self.fields:
			s += "\t" + f.to_string() + "\n"
		return s
		
class Select(FormField):
	def __init__(self, name, attrs):
		super().__init__(name, "select", attrs)
		self.options = []
	def to_string(self):
		s = "select attributes: " + str(self.attrs) + " options:"
		s += "None\n" if len(self.options) == 0 else "\n"
		for o in self.options:
			s += "\t\t" + o.to_string() + "\n"
		return s

class Option:
	def __init__(self, attrs):
		self.attrs = attrs
	def to_string(self):
		return "option attributes: " + str(self.attrs)

class Button(FormField):
	def __init__(self, name, attrs):
		super().__init__(name, "button", attrs)
	def to_string(self):
		return "button attributes: " + str(self.attrs)
		
class Textarea(FormField):
	def __init__(self, name, attrs):
		super().__init__(name, "textarea", attrs)
	def to_string(self):
		return "textarea attributes: " + str(self.attrs)

class DiscovererParser(HTMLParser):
	
	def __init__(self):
		super().__init__()
		self.forms = []
		self.current_form = None
		self.current_select = None
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
	
	###################################################################
	
	def handle_form_start(self, attrs):
		f = Form(attrs.get("action", "."), attrs.get("method", "GET"))
		self.forms.append(f)
		self.current_form = f
		
	def handle_form_end(self):
		self.current_form = None
	
	def handle_select_start(self, attrs):
		s = Select(attrs.get("name",""),attrs)
		self.add_field_to_form(s)
		self.current_select = s
		
	def handle_select_end(self):
		self.current_select = None

	def handle_option(self,attrs):
		o = Option(attrs)
		if self.current_select:
			self.current_select.options.append(o)
		
	def handle_input(self, attrs):
		field = FormField(attrs.get("name", ""), attrs.get("type", "text"), attrs)
		self.add_field_to_form(field)
	
	def handle_link(self, attrs):
		l = attrs.get("href","")
		if len(l) > 0:
			self.links.append(l)
	
	def handle_button(self,attrs):
		b = Button(attrs.get("name",""), attrs)
		self.add_field_to_form(b)
	
	def handle_textarea(self,attrs):
		ta = Textarea(attrs.get("name",""), attrs)
		self.add_field_to_form(ta)
	
	def add_field_to_form(self, field):
		if not self.current_form:
			self.fields.append(field)
		else:
			self.current_form.fields.append(field)


# parser = DiscovererParser()
# parser.feed('<form><input some="a" some2="b">Test</input>'
            # '<input>Test2</input></form><form>'
			  # '<select><option label="testa"/><option label="testb"/>'
			  # '</select><select></select></form><form></form>')
# parser.close()
# for f in parser.forms:
	# print(f.to_string())