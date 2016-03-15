from model.dataProviderFactory import *
from view.view import *
import datetime

SHOWCASE_TRAIN = "24114"

class Controller():
	myView = None
	myModel = None
	request = None
	response = None

	def __init__(self, request, response):
		self.request = request
		self.response = response
		self.buildNLS()

	def isMobileClient(self):
		return True

	def buildNLS(self):
		key = 'Accept-Language'
		if self.request.headers.has_key(key):
			langSupport.setLang(self.request.headers[key])
		else:
			langSupport.setLang('')

	def getViewAction(self, theDate, trainId):
		self.response.headers['Content-Type'] = 'text/html;'
		self.myView.theDate = theDate
		self.myView.trainId = trainId
		self.response.out.write(self.myView.render(self.isMobileClient()))

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
		self.getViewAction(theDate, SHOWCASE_TRAIN)

	def getLastDatetime(self):
		if datetime.datetime.now().time() > datetime.time(23,05,0):
			theDate = date.today()
		else:
			#today = datetime.datetime.strptime(datetime.datetime.today(), "%Y-%m-%d")
			today = datetime.datetime.today()
			theDate = today - datetime.timedelta(days = 1)
		return theDate

	def post(self):
		#implement redirection o home
		pass

'''
Used for static pages generation
'''
class DummyController(Controller):

	def get(self):
		self.response.headers['Content-Type'] = 'text/html;'
		self.response.out.write(self.myView.render(self.isMobileClient()))


class ConsoleController(Controller):

	def __init__(self, request, response):
		self.request = request
		self.response = response

	def getViewAction(self):
		self.response.headers['Content-Type'] = 'text/html;'
		self.response.out.write(self.myView.render(self.isMobileClient()))

	def get(self):
		self.getViewAction()

	def post(self):
		trainId = self.request.get('trainNum')
		trainType = self.request.get('type')
		fromStation = self.request.get('leaveStation')
		toStation = self.request.get('endStation')
		arrival = self.request.get('arriveTime')
		departure = self.request.get('leaveTime')
		URL = self.request.get('url')
		notes = self.request.get('notes')
		if trainId and trainType and fromStation and toStation and arrival and departure and URL != 'None':
			newSurvey = self.myModel.findTrainDescrById(trainId)
			newSurvey.trainId = trainId
			newSurvey.type = trainType
			newSurvey.leaveStation = fromStation
			newSurvey.endStation = toStation
			newSurvey.arriveTime = arrival
			newSurvey.leaveTime = departure
			newSurvey.date = datetime.datetime.today()
			newSurvey.status = 'enabled'
			newSurvey.url = URL
			newSurvey.notes = notes
			newSurvey.put()
		self.getViewAction()
