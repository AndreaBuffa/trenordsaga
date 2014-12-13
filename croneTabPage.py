import webapp2
from dataProviderFactory import DataProviderFactory,ChroneTab
from scheduleParser import ScheduleParser

class CroneTabPage(webapp2.RequestHandler):
	def get(self):
		self.response.headers['Content-Type'] = 'text/plain'
		self.response.write('Hello, chornetab!')
		myFactory = ChroneTab()
		myData = myFactory.createDataProvider()
		#HTTPException
		buffer = myData.RetrieveSourcePage()

		if buffer != None:
			myParser = ScheduleParser(buffer)
				#print myParser.GetTimings()
			self.response.write(myParser.GetTimings())
		self.response.write(buffer)


app = webapp2.WSGIApplication([
    ('/', CroneTabPage),
], debug=True)

