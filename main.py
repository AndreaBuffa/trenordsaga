import webapp2
from controller import *

class HandleRequest(webapp2.RequestHandler):

	def get(self, trainId="", date=""):
		appFactory = FrontEndFactory()
		app = appFactory.create(self.request, self.response)
		myController = app.getController()
		myController.myView = app.getView()
		return myController.get()

	def post(self):
		appFactory = FrontEndFactory()
		app = appFactory.create(self.request, self.response)
		myController = app.getController()
		myController.myView = app.getView()
		return myController.post()

class AppFactory:
	""" follows the abstract class patterns """
	def create(self):
		return

class FrontEndFactory(AppFactory):

	def create(self, request, response):
		if re.compile('^\/about').search(request.path):
			return StaticPage(request, response)
		elif re.compile('^\/stats').search(request.path):
			return ClientEndpoint(request, response)
		else:
			return DynamicPage(request, response)

class MVC:
	myView = None
	request = None
	response = None

	def __init__(self, request, response):
		self.request = request
		self.response = response

	def getController(self):
		return

	def getView(self):
		return

	def getModel(self):
		return

class DynamicPage(MVC):
	""" Provides a common synchronous client/server app """
	def getController(self):
		controller = DayController(self.request, self.response)
		return controller

	def getView(self):
		if not self.myView:
			self.myView = ScheduleViewer(self.getModel())
		return self.myView

	def getModel(self):
		myFactory = DataStore()
		return myFactory.createDataProvider()

class StaticPage(MVC):
	""" Provides a static content. Model is None. """
	def getController(self):
		controller = DummyController(self.request, self.response)
		return controller

	def getView(self):
		if not self.myView:
			self.myView = StaticView(self.getModel())
		return self.myView

	def getModel(self):
		return None

class ClientEndpoint(StaticPage):
	""" Provides a client endpoint for querying the server API"""
	def getView(self):
		if not self.myView:
			self.myView = ContainerView(self.getModel())
		return self.myView


app = webapp2.WSGIApplication([
	(r'/survey', HandleRequest),
	(r'/console/(\d)+/(\d{4}-\d{1,2}-\d{1,2})', ConsoleController),
	(r'/about', HandleRequest),
	(r'/stats', HandleRequest),
	(r'/', HandleRequest)
])
