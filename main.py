import webapp2
from controller import *

class HandleRequest(webapp2.RequestHandler):

	def get(self, trainId="", y="", m="", d=""):
		appFactory = FrontEndFactory()
		app = appFactory.create(self.request, self.response)
		myController = app.getController()
		myController.myView = app.getView()
		myController.myModel = app.getModel()
		return myController.get()

	def post(self):
		appFactory = FrontEndFactory()
		app = appFactory.create(self.request, self.response)
		myController = app.getController()
		myController.myView = app.getView()
		myController.myModel = app.getModel()
		return myController.post()

class AppFactory:
	""" follows the abstract class patterns """
	def create(self):
		return

class FrontEndFactory(AppFactory):

	def create(self, request, response):
		if re.compile('^\/about').search(request.path):
			return StaticApp(request, response)
		elif re.compile('^\/stats').search(request.path):
			return ClientEndpoint(request, response)
		elif re.compile('^\/surveys').search(request.path):
			return ClientEndpoint(request, response)
		elif re.compile('^\/search').search(request.path):
			return ClientEndpoint(request, response)
		elif re.compile('^\/console').search(request.path):
			return AdminApp(request, response)
		else:
			return DynamicApp(request, response)

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

class DynamicApp(MVC):
	""" Provides a common synchronous client/server app """
	def getController(self):
		controller = Controller(self.request, self.response)
		return controller

	def getView(self):
		if not self.myView:
			self.myView = HomePageView(self.getModel(), {})
		return self.myView

	def getModel(self):
		myFactory = DataStore()
		return myFactory.createDataProvider()

class StaticApp(MVC):
	""" Provides a static content. Model is None. Can manage query-string"""
	def getController(self):
		controller = QueryStringController(self.request, self.response)
		return controller

	def getView(self):
		if not self.myView:
			self.myView = StaticView(self.getModel(), {})
		return self.myView

	def getModel(self):
		return None

class ClientEndpoint(StaticApp):
	""" Provides a client endpoint for querying the server API"""
	def getView(self):
		if not self.myView:
			self.myView = OnePageAppView(self.getModel(), self.request)
		return self.myView

	def getModel(self):
		myFactory = DataStore()
		return myFactory.createDataProvider()

class AdminApp(DynamicApp):

	def getController(self):
		controller = ConsoleController(self.request, self.response)
		return controller

	def getView(self):
		if not self.myView:
			self.myView = ConsoleView(self.getModel(), {})
		return self.myView


app = webapp2.WSGIApplication([
	(r'/surveys', HandleRequest),
	(r'/console', HandleRequest),
	(r'/about', HandleRequest),
	(r'/stats', HandleRequest),
	(r'/search', HandleRequest),
	(r'/', HandleRequest)
])
