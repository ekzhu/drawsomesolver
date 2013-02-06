import os
from google.appengine.ext.webapp import template
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from django.utils import simplejson
import solver

class MainPage(webapp.RequestHandler):
	def get(self):
		length_range = [str(i) for i in range(3,13)]
		template_values = {'length_range': length_range}
		path = os.path.join(os.path.dirname(__file__), 'index.html')
		self.response.out.write(template.render(path, template_values))
	
	# def post(self):
	# 	letters = self.request.get('content')
	# 	length = int(self.request.get('length'))
	# 	if len(letters) > 12 or length > 12:
	# 		solutions = ['Too Long']
	# 	elif len(letters) < 3 or length < 3:
	# 		solutions = ['Too Short']
	# 	else:
	# 		solutions = solver.findwords(letters, length)
	# 	if not solutions:
	# 		solutions = ['No Word Found']
	# 	length_range = [str(i) for i in range(3,13)]
	# 	template_values = { 'solutions': solutions, 'length_range': length_range}
	# 	path = os.path.join(os.path.dirname(__file__), 'index.html')
	# 	self.response.out.write(template.render(path, template_values))

class RPCHandler(webapp.RequestHandler):
	def __init__(self):
		webapp.RequestHandler.__init__(self)
		self.methods = RPCMethods()
	
	def get(self):
		func = None
		action = self.request.get('action')
		if action:
			if action[0] == '_':
				self.error(403) # access denied
				return
			else:
				func = getattr(self.methods, action, None)
		if not func:
			self.error(404) # file not found
			return
		args = ()
		while True:
			key = 'arg%d' % len(args)
			val = self.request.get(key)
			if val:
				args += (simplejson.loads(val),)
			else:
				break
		result = func(*args)
		self.response.out.write(simplejson.dumps(result))
	
class RPCMethods:
	def FindWords(self, *args):
		# The JSON encoding may have encoded integers as strings.
		# Be sure to convert args to any mandatory type(s).
		letters = str(args[0])
		letters = "".join(letters.split())
		length = int(args[1])
		if len(letters) > 12 or length > 12:
			solutions = ['Too Long']
		elif len(letters) < 3 or length < 3 or len(letters) < length:
			solutions = ['Too Short']
		else:
			solutions = solver.findwords(letters, length)
		if not solutions:
			solutions = ['No Word Found']
		output = ""
		for word in solutions:
			output += "<tr><td>%s</td><tr>" % word
		return output

def main():
	application = webapp.WSGIApplication([('/', MainPage), ('/rpc', RPCHandler),], debug=True)
	run_wsgi_app(application)


if __name__ == '__main__':
	main()