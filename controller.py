import webapp2
from model.dataProviderFactory import *
from view.view import *
import datetime

class Controller(webapp2.RequestHandler):
	myView = None

	def __init__(self, request, response):
		self.initialize(request, response)
		self.buildView()
		self.buildNLS()

	def buildView(self):
		myFactory = DataStore()
		myDataModel = myFactory.createDataProvider()
		self.myView = StatsView(myDataModel)

	def buildNLS(self):
		langSupport.setLang(self.request.headers['Accept-Language'])

	def getViewAction(self, theDate):
		self.response.headers['Content-Type'] = 'text/html;'
		self.myView.theDate = theDate
		self.response.out.write(self.myView.render())

	def get(self):
		self.getViewAction()

	def getLastDatetime(self):
		if datetime.datetime.now().time() > datetime.time(23,05,0):
			theDate = date.today()
		else:
			#today = datetime.datetime.strptime(datetime.datetime.today(), "%Y-%m-%d")
			today = datetime.datetime.today()
			theDate = today - datetime.timedelta(days = 1)
		return theDate

class SimpleController(Controller):

	def __init__(self, request, response):
		super(SimpleController, self).__init__(request, response)
		#print self.request.path
		#print webapp2.get_request().path

	def buildView(self):
		self.myView = SimpleView()

	def getViewAction(self):
		self.response.headers['Content-Type'] = 'text/html;'
		self.response.out.write(self.myView.render())

	def get(self):
		self.getViewAction()

class DayController(Controller):

	def getViewAction(self, theDate):
		self.response.headers['Content-Type'] = 'text/html;'
		self.myView.theDate = theDate
		self.response.out.write(self.myView.render())

	def get(self):
		self.getViewAction(self.getLastDatetime())

	def get(self, year="", month="", day=""):

		if year and month and day:
			try:
				theDate = datetime.datetime.strptime(year+"-"+month+"-"+day, "%Y-%m-%d").date()
			except ValueError:
				theDate = self.getLastDatetime()
		else:
			theDate = self.getLastDatetime()
		if re.compile('^\/(\w)+').search(self.request.path):
			self.myView.showBanner = False;
		else:
			self.myView.showBanner = True;
		self.getViewAction(theDate)

	def post(self):
		try:
			theDate = datetime.datetime.strptime(self.request.get("datetime"), "%Y-%m-%d").date()
		except ValueError:
			theDate = self.getLastDatetime()
		self.myView.showBanner = False;
		self.getViewAction(theDate)


class ConsoleController(Controller):

	def __init__(self):
		myFactory = DataStore()
		myDataModel = myFactory.createDataProvider()
		self.myView = ScheduleValidator(myDataModel)

	def get(self, trainId="", date=""):
		if date:
			try:
				theDate = datetime.datetime.strptime(date, "%Y-%m-%d").date()
			except ValueError:
				theDate = self.getLastDatetime()
		else:
			theDate = self.getLastDatetime()
		self.getViewAction(theDate)
