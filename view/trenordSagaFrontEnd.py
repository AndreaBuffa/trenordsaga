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
		if year and month and day:
			try:
				theDate = datetime.datetime.strptime(year+"-"+month+"-"+day, "%Y-%m-%d").date()
			except:
				theDate = date.today()
		else:
			theDate = date.today()

		buffer = self.myModel.RetrieveSourcePage(theDate)
		if buffer:
			myParser = ScheduleParser(buffer)
			timeSchedule = myParser.GetTimings()
			myFormatter = Formatter()
			chartData = myFormatter.ToLineChartJSon(timeSchedule)

			stationsByDelay = sorted(timeSchedule, key=lambda station: station['delay_m'], reverse=True)
			onDelayStations = filter(lambda station: station['delay_m'] > 0, stationsByDelay)
			onTimeStations = filter(lambda station: station['delay_m'] <= 0, stationsByDelay)
			stationsByDelayJS = myFormatter.ToHistogramJSon(onDelayStations)

			path = os.path.join(os.path.dirname(__file__), 'tpl/stats2.html')
			return template.render(path, {'stations': chartData,
				'date': theDate,
				'stationsByDelay': stationsByDelayJS,
				'onTimeStations': onTimeStations});

class ScheduleValidator(TrenordSagaFrontEnd):
	def Render(self, year="", month="", day=""):
		return ""

