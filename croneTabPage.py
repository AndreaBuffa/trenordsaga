import webapp2
from dataProviderFactory import DataProviderFactory,ChroneTab

class CroneTabPage(webapp2.RequestHandler):
	def get(self):
		self.response.headers['Content-Type'] = 'text/plain'
		self.response.write('Hello, chornetab!')
		myFactory = ChroneTab()
		myData = myFactory.createDataProvider()
		buffer = myData.RetrieveSourcePage()
		#self.response.write(buffer)
		#if buffer != None:

app = webapp2.WSGIApplication([
    ('/', CroneTabPage),
], debug=True)

