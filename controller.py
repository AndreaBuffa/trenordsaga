import webapp2
from model.dataProviderFactory import *
from view.trenordSagaFrontEnd import *
import datetime

class Controller(webapp2.RequestHandler):

	def build(self):
		myFactory = FrontEnd()
		myDataModel = myFactory.createDataProvider()
		self.myView = StatsView(myDataModel)
		langSupport.setLang(self.request.headers['Accept-Language'])

	def get(self):
		self.build()
		self.response.headers['Content-Type'] = 'text/html;'
		self.response.out.write(self.myView.render(date.today()))

class DayController(Controller):

	def get(self, year="", month="", day=""):
		if year and month and day:
			try:
				theDate = datetime.datetime.strptime(year+"-"+month+"-"+day, "%Y-%m-%d").date()
			except ValueError:
				theDate = date.today()
		else:
			theDate = date.today()
		self.build()
		self.myView.showBanner = 0;
		self.response.headers['Content-Type'] = 'text/html;'
		self.response.out.write(self.myView.render(theDate))
