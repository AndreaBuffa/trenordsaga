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

	def getViewAction(self, theDate):
		self.response.headers['Content-Type'] = 'text/html;'
		self.response.out.write(self.myView.render(theDate))

	def get(self):
		self.build()
		self.getViewAction(self.getLastDatetime())

	def getLastDatetime(self):
		if datetime.datetime.now().time() > datetime.time(10,11,0):
			theDate = date.today()
		else:
			#today = datetime.datetime.strptime(datetime.datetime.today(), "%Y-%m-%d")
			today = datetime.datetime.today()
			theDate = today.replace(day=today.day - 1)
		return theDate

class DayController(Controller):

	def get(self, year="", month="", day=""):
		self.build()
		self.myView.showBanner = 0;
		if year and month and day:
			try:
				theDate = datetime.datetime.strptime(year+"-"+month+"-"+day, "%Y-%m-%d").date()
			except ValueError:
				theDate = self.getLastDatetime()
		else:
			theDate = self.getLastDatetime()
		self.getViewAction(theDate)

	def post(self):
		try:
			theDate = datetime.datetime.strptime(self.request.get("datetime"), "%Y-%m-%d").date()
		except ValueError:
			theDate = self.getLastDatetime()
		self.build()
		self.myView.showBanner = 0;
		self.getViewAction(theDate)
