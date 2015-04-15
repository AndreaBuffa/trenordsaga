import os
from google.appengine.ext.webapp import template
from formatter import *
from scheduleParser import *
from nls.nls import *

class View:
	myModel = None
	showBanner = False
	pageBuffer = b""
	localPath = ""

	def __init__(self, aModel):
		self.myModel = aModel
		self.showBanner = True
		self.localPath = os.path.dirname(__file__)

	def renderTpl(self, path="", dataToBind={}):
		if path != "":
			self.pageBuffer += template.render(os.path.join(self.localPath, path), dataToBind)

	def render(self, theDate):
		return ""

class StatsView(View):

	def render(self, theDate):
		chartData = []
		onTimeStations = []
		stationsByDelayJS = ""
		pieJS = ""
		buffer = self.myModel.retrieveSourcePage('24114', theDate)
		if buffer:
			myParser = ScheduleParser(buffer)
			timeSchedule = myParser.GetTimings()
			myFormatter = Formatter()
			chartData = myFormatter.ToLineChartJSon(timeSchedule)

			stationsByDelay = sorted(timeSchedule,
				key=lambda station: station['delay_m'],
				reverse=True)
			onDelayStations = filter(lambda station: station['delay_m'] > 0,
				stationsByDelay)
			onTimeStations = filter(lambda station: station['delay_m'] <= 0,
				stationsByDelay)

			stationsByDelayJS = myFormatter.ToColumnChartJSon(onDelayStations)

		self.renderTpl('tpl/head.html', {'nls': langSupport.getEntries(),
			'stations': chartData,
			'date': theDate,
			'stationsByDelay': stationsByDelayJS})

		self.renderTpl('tpl/bodyHeader.html', {'nls': langSupport.getEntries(),
			'landingClass': self.showBanner})

		if self.showBanner:
			self.renderTpl('tpl/banner.html', {'nls': langSupport.getEntries()})

		if buffer:
			self.renderTpl('tpl/survey.html', {'nls': langSupport.getEntries(),
				'onTimeStations': onTimeStations,
				'date': theDate});
		else:
			self.renderTpl('tpl/nosurvey.html', {'nls': langSupport.getEntries(),
				'date': theDate});

		self.renderTpl('tpl/footer.html', {'nls': langSupport.getEntries()})

		return self.pageBuffer

class ScheduleValidator(View):
	def render(self, theDate):
		#buffer = self.myModel.retrieveSourcePage('24114', theDate)
		return ""

