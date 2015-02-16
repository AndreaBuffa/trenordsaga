import webapp2
from model.dataProviderFactory import *
from view.trenordSagaFrontEnd import *

class MainPage(webapp2.RequestHandler):
    def get(self, year="", month="", day=""):
		self.response.headers['Content-Type'] = 'text/html;'
		myFactory = FrontEnd()
		myDataModel = myFactory.createDataProvider()
		myView = StatsView(myDataModel)
		self.response.out.write(myView.Render(year, month, day))

app = webapp2.WSGIApplication([
	(r'/(\d{4})/(\d{2})/(\d{2})', MainPage),
	(r'/.*', MainPage),
])
