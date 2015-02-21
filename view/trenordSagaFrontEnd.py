import os
from google.appengine.ext.webapp import template
from formatter import *
from scheduleParser import *

class TrenordSagaFrontEnd:
	myModel = None
	showBanner = 0

	def __init__(self, aModel):
		self.myModel = aModel
		self.showBanner = 1


	def Render(self, theDate):
		return ""

class StatsView(TrenordSagaFrontEnd):

	def __init__(self, aModel):
		self.myModel = aModel

	def Render(self, theDate):

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
	def Render(self, theDate):
		return ""

