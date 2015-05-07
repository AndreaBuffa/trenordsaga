import webapp2
from controller import *

app = webapp2.WSGIApplication([
	(r'/survey/', DayController),
	(r'/survey', DayController),
	(r'/console/(\d)+/(\d{4}-\d{1,2}-\d{1,2})', ConsoleController),
	(r'/about', SimpleController),
	(r'/', DayController)
])
