import webapp2
from model.dataProviderFactory import *
from view.trenordSagaFrontEnd import *
import datetime

class MainPage(webapp2.RequestHandler):
	def get(self, year="", month="", day=""):

		langSupport.setLang(self.request.headers['Accept-Language'])
		#langSupport.setLang("en-US")
		if year and month and day:
			try:
				theDate = datetime.datetime.strptime(year+"-"+month+"-"+day, "%Y-%m-%d").date()
			except ValueError:
				theDate = date.today()
		else:
			theDate = date.today()

		self.response.headers['Content-Type'] = 'text/html;'
		myFactory = FrontEnd()
		myDataModel = myFactory.createDataProvider()
		myView = StatsView(myDataModel)
		self.response.out.write(myView.Render(theDate))

app = webapp2.WSGIApplication([
	(r'/(\d{4})/(\d{2})/(\d{2})', MainPage),
	(r'/.*', MainPage),
])
