import webapp2
import dataProvider
from dataProviderFactory import DataProviderFactory,FrontEnd
from scheduleParser import ScheduleParser
from formatter import Formatter
import os
from google.appengine.ext.webapp import template

class MainPage(webapp2.RequestHandler):
    def get(self, year="", month="", day=""):
		self.response.headers['Content-Type'] = 'text/html;'

		print year
		print month
		print day
		myFactory = FrontEnd()
		myData = myFactory.createDataProvider()
		buffer = myData.RetrieveSourcePage(year, month, day)
		if buffer:
			myParser = ScheduleParser(buffer)
			myFormatter = Formatter(myParser.GetTimings())
			chartData = myFormatter.ToGChartsDataTable()
			path = os.path.join(os.path.dirname(__file__), 'stats.html')
			self.response.out.write(template.render(path, {'stations': chartData}))

#self.response.write(buffer)


#print "debug"
#app = webapp2.WSGIApplication([
#	('/.*', MainPage),
#	webapp2.Route(r'<:\d{4}>/<:\d{2}/:\d{2}>', handler=MainPage, name='stats'),
#], debug=True)

app = webapp2.WSGIApplication([
	(r'/(\d{4})/(\d{2})/(\d{2})', MainPage),
	(r'/.*', MainPage),
])