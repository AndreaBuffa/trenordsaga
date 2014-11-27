import webapp2
import dataProviderFactory

class CroneTabPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('Hello, chornetab!')

	myFactory = ChroneTab()
	myData = myFactory.createDataProvider()
	buffer = myData.RetrieveSourcePage()

app = webapp2.WSGIApplication([
    ('/', CroneTabPage),
], debug=True)

