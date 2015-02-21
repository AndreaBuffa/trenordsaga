import webapp2
from controller import DayController

app = webapp2.WSGIApplication([
	(r'/survey/(\d{4})/(\d{2})/(\d{2})', DayController),
	(r'/survey/', DayController),
	(r'/survey', DayController)
])
