import os
from google.appengine.ext.webapp import template
from nls.nls import *
import webapp2

TPL_PATH = "/tpl/"
JS_PATH = "/../js/client-side-mvc/"

class View:
	myModel = None
	showBanner = False
	renderForMobile = True
	pageBuffer = b""
	tplPath = ""
	jsPath = ""

	def __init__(self, aModel, request):
		self.myModel = aModel
		self.showBanner = True
		self.tplPath = os.path.dirname(__file__) + TPL_PATH
		self.jsPath = os.path.dirname(__file__) + JS_PATH
		self.request = request

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
		self.renderForMobile = isMobileClient
		self.prepare()
		return self.pageBuffer

	def prepare(self):
		pass

class StaticView(View):

	def prepare(self):
		self.renderTpl('head.html', {
			'nls': langSupport.getEntries(),
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
			'nls': langSupport.getEntries(),
			'renderForMobile': self.renderForMobile})

		self.pageBuffer += '<script type="text/Javascript">'
		self.embedJS('common.js', {'nls': langSupport.getEntries()})
		self.embedJS('model.js', {})
		import re
		if re.compile('^\/search').search(self.request.path):
			self.embedJS('view-add-train.js', {})
			self.embedJS('add-train-app.js', {})
		else:
			self.embedJS('view-tab-view.js', {})
			self.embedJS('view-type-picker.js', {'nls': langSupport.getEntries()})
			self.embedJS('view-num-picker.js', {'nls': langSupport.getEntries()})
			self.embedJS('view-search.js', {})

			if re.compile('^\/surveys').search(self.request.path):
				self.embedJS('view-date-picker.js', {'nls': langSupport.getEntries()})
				self.embedJS('view-surveys.js',
							 {'nls': langSupport.getEntries()})
				self.embedJS('survey-app.js', {})
			else:
				self.embedJS('view-display-stats.js',
				             {'nls': langSupport.getEntries()})
				self.embedJS('stats-app.js', {})

		self.embedJS('api-endpoint.js', {})
		self.pageBuffer += '</script>'

		self.renderTpl('bodyHeader.html', {'nls': langSupport.getEntries(),
			'landingClass': False})
		if re.compile('^\/surveys').search(self.request.path):
			self.renderTpl('survey.html', {'nls': langSupport.getEntries()})
		elif re.compile('^\/search').search(self.request.path):
			self.renderTpl('search.html', {'nls': langSupport.getEntries()})
		else:
			self.renderTpl('stats.html', {'nls': langSupport.getEntries()})
		self.renderTpl('footer.html', {'nls': langSupport.getEntries()})


class HomePageView(View):
	trainId = None
	theDate = None

	def prepare(self):
		chartData = []
		onTimeStations = []
		stationsByDelayJS = ""
		pieJS = ""
		buffer = self.myModel.retrieveSourcePage(self.trainId, self.theDate)
		if buffer:
			from utils.parser import ScheduleParser
			myParser = ScheduleParser(buffer)
			timeSchedule = myParser.GetTimings()
			from formatter import toLineChartJSon
			chartData = toLineChartJSon(timeSchedule)

			stationsByDelay = sorted(timeSchedule,
				key=lambda station: station['delay_m'],
				reverse=True)

			onTimeStations = filter(
				lambda station: station['delay_m'] <= 0,
				timeSchedule)


			stops = self.myModel.findAllTrainStopById(self.trainId)
			delayDict = {}
			for trainStop in stops:
				delayDict[trainStop.name] = trainStop.getMedianValue(
					trainStop.getDelayList(True, True))
			from formatter import toColumnChartJSon
			stationsByDelayJS = toColumnChartJSon(timeSchedule,
			                                      delayDict, self.theDate)

		trainDescr = self.myModel.findTrainDescrById(self.trainId)
		trainType = leaveTime = startSurveyDate = '';
		if trainDescr:
			trainType = trainDescr.type
			leaveTime = trainDescr.leaveTime
			startSurveyDate = trainDescr.getIsoFormatDate()

		self.renderTpl('surveyHead.html', {
		               'nls': langSupport.getEntries(),
		               'renderForMobile': self.renderForMobile})

		self.renderTpl('bodyHeader.html', {
			'nls': langSupport.getEntries(),
			'landingClass': self.showBanner})

		if self.showBanner:
			self.renderTpl('banner.html', {
			               'nls': langSupport.getEntries()
			               })
		self.pageBuffer += '<script type="text/Javascript">'
		self.embedJS('common.js', {'nls': langSupport.getEntries()})
		self.embedJS('view-surveys.js', {'nls': langSupport.getEntries()})
		self.pageBuffer += '</script>'

		if buffer:
			self.renderTpl('survey-home.html', {
			               'nls': langSupport.getEntries(),
			               'onTimeStations': onTimeStations,
		                   'stationsByDelay': stationsByDelayJS,
		                   'stations': chartData,
			               'date': self.theDate.strftime('%Y-%m-%d'),
			               'trainId': self.trainId,
			               'trainType': trainType,
		                   'leaveTime' : leaveTime})
		else:
			self.renderTpl('nosurvey.html', {
			               'nls': langSupport.getEntries(),
			               'date': self.theDate,
			               'trainId': self.trainId})

		self.renderTpl('footer.html', {'nls': langSupport.getEntries()})


class ConsoleView(View):

	def prepare(self):
		requests = self.myModel.getNewSurvey()
		self.renderTpl('admin/new.html', {
		               'requests': requests
		               })

class ScheduleValidator(View):
	def render(self):
		#buffer = self.myModel.retrieveSourcePage('24114', theDate)
		return ""
