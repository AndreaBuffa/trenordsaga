import webapp2
from dataProviderFactory import DataProviderFactory,ChroneTab
from s9 import S9

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

