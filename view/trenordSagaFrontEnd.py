import os
from google.appengine.ext.webapp import template
from formatter import *
from scheduleParser import *

class TrenordSagaFrontEnd:
	myModel = None

	def __init__(self, aModel):
		self.myModel = aModel

	def Render(self, year="", month="", day=""):
		return ""

class StatsView(TrenordSagaFrontEnd):

	def __init__(self, aModel):
		self.myModel = aModel

	def Render(self, year="", month="", day=""):
		buffer = self.myModel.RetrieveSourcePage(year, month, day)
		if buffer:
			myParser = ScheduleParser(buffer)
			myFormatter = Formatter(myParser.GetTimings())
			chartData = myFormatter.ToGChartsDataTable()
			path = os.path.join(os.path.dirname(__file__), 'tpl/stats.html')
			return template.render(path, {'stations': chartData});

class ScheduleValidator(TrenordSagaFrontEnd):
	def Render(self, year="", month="", day=""):
		return ""

