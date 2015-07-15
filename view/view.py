import os
from google.appengine.ext.webapp import template
from formatter import *
from scheduleParser import *
from nls.nls import *
import webapp2
import re

TPL_PATH = "/tpl/"
JS_PATH = "/../js/client-side-mvc/"

class View:
	myModel = None
	showBanner = False
	renderForMobile = True
	pageBuffer = b""
	tplPath = ""
	jsPath = ""

	def __init__(self, aModel):
		self.myModel = aModel
		self.showBanner = True
		self.tplPath = os.path.dirname(__file__) + TPL_PATH
		self.jsPath = os.path.dirname(__file__) + JS_PATH

	def renderTpl(self, path="", dataToBind={}):
		if path:
			self.pageBuffer += template.render(
				os.path.join(self.tplPath, path),
				dataToBind)

	def embedJS(self, path="", dataToBind={}):
		if path:
			self.pageBuffer += template.render(
				os.path.join(self.jsPath, path),
				dataToBind)

	def render(self, isMobileClient):
		#self.renderForMobile = isMobileClient
		self.prepare()
		return self.pageBuffer

	def prepare(self):
		pass

class StaticView(View):

	def __init__(self, aModel):
		View.__init__(self, None)

	def prepare(self):
		self.renderTpl('head.html', {
			'renderForMobile': self.renderForMobile})
		self.pageBuffer += "</head>"
		self.renderTpl('bodyHeader.html', {
			'nls': langSupport.getEntries(),
			'landingClass': False})

		self.renderTpl(webapp2.get_request().path[1:] + '_' +
			langSupport.currLang + '.html',
			{'nls': langSupport.getEntries(),
			 'landingClass': self.showBanner})

		self.renderTpl('footer.html', {'nls': langSupport.getEntries()})


class OnePageAppView(StaticView):

	def prepare(self):
		self.renderTpl('head.html', {
			'renderForMobile': self.renderForMobile})

		self.pageBuffer += '<script type="text/Javascript">'
		self.embedJS('view-choose-train.js', {})
		self.embedJS('view-display-stats.js', {})
		self.embedJS('model.js', {})
		self.embedJS('stats-app.js', {})
		self.embedJS('api-endpoint.js', {})
		self.pageBuffer += '</script>'

		self.renderTpl('bodyHeader.html', {'nls': langSupport.getEntries(),
			'landingClass': False})
		self.pageBuffer += '<section class="wrapper"><section class="container">'
		self.pageBuffer += '<div id="outputLog"></div>'
		self.pageBuffer += '</section></section>'
		self.renderTpl('footer.html', {'nls': langSupport.getEntries()})


class ScheduleViewer(View):
	trainId = None
	theDate = None

	def __init__(self, aModel):
		View.__init__(self, aModel)

	def prepare(self):
		chartData = []
		onTimeStations = []
		stationsByDelayJS = ""
		pieJS = ""
		buffer = self.myModel.retrieveSourcePage(self.trainId, self.theDate)
		if buffer:
			myParser = ScheduleParser(buffer)
			timeSchedule = myParser.GetTimings()
			myFormatter = Formatter()
			chartData = myFormatter.ToLineChartJSon(timeSchedule)

			stationsByDelay = sorted(timeSchedule,
				key=lambda station: station['delay_m'],
				reverse=True)
			onDelayStations = filter(
				lambda station: station['delay_m'] > 0,
				stationsByDelay)
			onTimeStations = filter(
				lambda station: station['delay_m'] <= 0,
				stationsByDelay)

			stationsByDelayJS = myFormatter.ToColumnChartJSon(
				onDelayStations)

		self.renderTpl('surveyHead.html', {
			'nls': langSupport.getEntries(),
			'stations': chartData,
			'date': self.theDate,
			'stationsByDelay': stationsByDelayJS,
			'renderForMobile': self.renderForMobile})

		self.renderTpl('bodyHeader.html', {
			'nls': langSupport.getEntries(),
			'landingClass': self.showBanner})

		if self.showBanner:
			self.renderTpl('banner.html', {
					'nls': langSupport.getEntries()
				})

		if buffer:
			self.renderTpl('survey.html', {
				'nls': langSupport.getEntries(),
				'onTimeStations': onTimeStations,
				'date': self.theDate,
				'trainId': self.trainId})
		else:
			self.renderTpl('nosurvey.html', {
				'nls': langSupport.getEntries(),
				'date': self.theDate,
				'trainId': self.trainId})

		self.pageBuffer += '<script type="text/Javascript">'
		self.embedJS('view-choose-train.js', {})
		self.embedJS('model.js', {})
		self.embedJS('survey-app.js', {
			'currDate': self.theDate,
			'minDate': self.myModel.findTrainDescrById(self.trainId).getIsoFormatDate()
			})
		self.embedJS('api-endpoint.js', {})
		self.pageBuffer += '</script>'

		self.renderTpl('footer.html', {'nls': langSupport.getEntries()})


class ScheduleValidator(View):
	def render(self):
		#buffer = self.myModel.retrieveSourcePage('24114', theDate)
		return ""

