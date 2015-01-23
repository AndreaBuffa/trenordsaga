import webapp2
from model.dataProviderFactory import *
import model.s9

class CroneTabPage(webapp2.RequestHandler):
	def get(self):
		self.response.headers['Content-Type'] = 'text/plain'
		self.response.write('Working...')
		myFactory = ChroneTab()
		myData = myFactory.createDataProvider()
		buffer = myData.RetrieveSourcePage()
		if buffer:
			timeSchedule = S9()
			timeSchedule.timings = buffer
			timeSchedule.put()
		self.response.write('Done!')

app = webapp2.WSGIApplication([
    ('/batch', CroneTabPage),
], debug=True)

