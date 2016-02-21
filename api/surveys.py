import endpoints
from protorpc import messages
from protorpc import message_types
from protorpc import remote
package = 'main_api'

class Train(messages.Message):
	""" Surveyed train class"""
	class Status(messages.Enum):
		SURVEYED = 1
		NOT_SURVEYED = 2
		UNDER_EVALUATION = 3

	trainId = messages.StringField(1)
	type = messages.StringField(2)
	leaveStation = messages.StringField(3)
	endStation = messages.StringField(4)
	arriveTime = messages.StringField(5)
	leaveTime = messages.StringField(6)
	surveyedFrom = messages.StringField(7)
	notes = messages.StringField(8)
	isSurveyed = messages.EnumField('Train.Status', 9, default='NOT_SURVEYED')

class TrainList(messages.Message):
	"""Collection of train objects"""
	items = messages.MessageField(Train, 1, repeated=True)

class SurveyGraphContainer(messages.Message):
	scheduled_real = messages.StringField(1)
	real_median = messages.StringField(2)

class DataSourceContainer(messages.Message):
	data = messages.StringField(1)

class Stop(messages.Message):
	""" Stop class"""
	stationName = messages.StringField(1)
	weekdayMedian = messages.FloatField(2)
	festiveMedian = messages.FloatField(3)
	allMedian = messages.FloatField(4)
	weekdaySamples = messages.IntegerField(5, repeated=True)
	weekdayCounters = messages.IntegerField(6, repeated=True)
	festiveSamples = messages.IntegerField(7, repeated=True)
	festiveCounters = messages.IntegerField(8, repeated=True)
	allSamples = messages.IntegerField(9, repeated=True)
	allCounters = messages.IntegerField(10, repeated=True)

class StopCollection(messages.Message):
	"""Collection of train Stop."""
	items = messages.MessageField(Stop, 1, repeated=True)

class Stats(messages.Message):
	graphData = messages.StringField(1)
	stopList = messages.MessageField(StopCollection, 2)

@endpoints.api(name='surveys', version='v1')
class SurveysApi(remote.Service):
	"""Surveys API v1. Allows to query the time schedule of each train
	for a particular date"""

	ID_RESOURCE = endpoints.ResourceContainer(
		message_types.VoidMessage)
	@endpoints.method(ID_RESOURCE, TrainList,
		path='list', http_method='GET',
		name='getList')
	def get_surveyed_collection(self, request):
		from model.dataProviderFactory import DataStore
		myFactory = DataStore()
		myDataModel = myFactory.createDataProvider()
		ret = TrainList()
		for trainDescr in myDataModel.findAllTrainDescr():
			ret.items.append(Train(
				trainId = trainDescr.trainId,
				type = trainDescr.type,
				leaveStation = trainDescr.leaveStation,
				endStation = trainDescr.endStation,
				arriveTime = trainDescr.arriveTime,
				leaveTime = trainDescr.leaveTime,
				surveyedFrom = str(trainDescr.date),
				notes = trainDescr.notes))

		return ret


	ID_RESOURCE = endpoints.ResourceContainer(
		message_types.VoidMessage,
		trainid=messages.StringField(1, variant=messages.Variant.STRING),
		year=messages.StringField(2, variant=messages.Variant.STRING),
		month=messages.StringField(3, variant=messages.Variant.STRING),
		day=messages.StringField(4, variant=messages.Variant.STRING))

	@endpoints.method(ID_RESOURCE, SurveyGraphContainer,
	                  path='survey/{trainid}/{year}/{month}/{day}',
	                  http_method='GET', name='getSurvey')
	def get_survey_graph_data(self, request):
		from model.dataProviderFactory import DataStore
		import utils.common
		from utils.parser import ScheduleParser
		from view.formatter import *
		ret = SurveyGraphContainer();
		tmpDate = [];
		if not utils.common.buildDate(request.year, request.month,
		                              request.day, tmpDate):
		        return ret
        #@todo check the date.
		myFactory = DataStore()
		myDataModel = myFactory.createDataProvider()
		buffer = myDataModel.retrieveSourcePage(request.trainid, tmpDate[0])
		if buffer:
			myParser = ScheduleParser(buffer)
			survey = myParser.GetTimings()
			ret.scheduled_real = toLineChartJSon(survey)

			stops = myDataModel.findAllTrainStopById(request.trainid)
			delayDict = {}
			for trainStop in stops:
				delayDict[trainStop.name] = trainStop.getMedianValue(
					trainStop.getDelayList(True, True))
			ret.real_median = toColumnChartJSon(survey, delayDict, tmpDate[0])
		return ret

	@endpoints.method(ID_RESOURCE, DataSourceContainer,
	                  path='source/{trainid}/{year}/{month}/{day}',
	                  http_method='GET', name='getSource')
	def get_train_data_source(self, request):
		import utils.common
		ret = DataSourceContainer();
		tmpDate = [];
		if not utils.common.buildDate(request.year, request.month,
		                              request.day, tmpDate):
			return ret
		from model.dataProviderFactory import DataStore
		myFactory = DataStore()
		myDataModel = myFactory.createDataProvider()
		ret.data = myDataModel.retrieveSourcePage(request.trainid,
		                                          tmpDate[0])
		return ret


	ID_RESOURCE = endpoints.ResourceContainer(
		message_types.VoidMessage,
		fromStation=messages.StringField(1, variant=messages.Variant.STRING),
		toStation=messages.StringField(2, variant=messages.Variant.STRING),
		when=messages.StringField(3, variant=messages.Variant.STRING),
		timeRange=messages.StringField(4, variant=messages.Variant.STRING))
	@endpoints.method(ID_RESOURCE, TrainList,
		path='search/{fromStation}/{toStation}/{when}/{timeRange}',
		http_method='GET',
		name='search')
	def search(self, request):
		import logging
		trainDescrList = TrainList()
		if (int(request.timeRange) < 1) or (int(request.timeRange) > 5):
			logging.debug('search_from_to: timeRange out of bound')
			return trainDescrList
		from model.dataProviderFactory import DataStore
		myFactory = DataStore()
		myDataModel = myFactory.createDataProvider()
		# query a third-party server
		serviceURL = myDataModel.getServiceURL('TrainListByStation')
		if not serviceURL:
			logging.debug('search_from_to: serviceURL not found!')
		import webscraper.scraper
		opener = webscraper.scraper.get_http_opener()

		trainListString = webscraper.scraper.get_train_list(opener,
							serviceURL,
							request.fromStation,
							request.toStation,
							request.when,
							request.timeRange)
		import utils.parser
		hrefList = utils.parser.extract_links(trainListString)

		trainList = webscraper.scraper.get_train_details(opener,
								 serviceURL,
								 hrefList)

		detailsList = utils.parser.extract_train_details(trainList)

		for train in detailsList:
			trainDescr = myDataModel.findTrainDescrById(train['number'])
			if trainDescr:
				surveyed = Train.Status.NOT_SURVEYED
				if trainDescr.status == 'enabled':
					surveyed = Train.Status.SURVEYED
				elif trainDescr.status == 'disabled':
					surveyed = Train.Status.UNDER_EVALUATION
				elif trainDescr.status == 'refused':
					surveyed = Train.Status.NOT_SURVED
				elif trainDescr.status == None:
					surveyed = Train.Status.SURVEYED
				else:
					surveyed = Train.Status.NOT_SURVED

				trainDescrList.items.append(Train(
					trainId = trainDescr.trainId,
					type = trainDescr.type,
					leaveStation = trainDescr.leaveStation,
					endStation = trainDescr.endStation,
					arriveTime = trainDescr.arriveTime,
					leaveTime = trainDescr.leaveTime,
					surveyedFrom = str(trainDescr.date),
					isSurveyed = surveyed))
			else:
				trainDescrList.items.append(Train(
					trainId = train['number'],
					type = train['type'],
					leaveStation = train['leave'],
					endStation = train['arrival'],
					arriveTime = train['arrivalTime'],
					leaveTime = train['leaveTime'],
					surveyedFrom = '',
					isSurveyed = Train.Status.NOT_SURVEYED))
		return trainDescrList

	ID_RESOURCE = endpoints.ResourceContainer(
		num=messages.StringField(1, variant=messages.Variant.STRING),
		trainType=messages.StringField(2, variant=messages.Variant.STRING),
		fromStation=messages.StringField(3, variant=messages.Variant.STRING),
		to=messages.StringField(4, variant=messages.Variant.STRING),
		leave=messages.StringField(5, variant=messages.Variant.STRING),
		arrive=messages.StringField(6, variant=messages.Variant.STRING))
	@endpoints.method(ID_RESOURCE, message_types.VoidMessage,
		path='survey/add/{num}/{trainType}/{fromStation}/{to}/{leave}/{arrive}',
		http_method='POST',
		name='addSurvey')
	def add_survey(self, request):
		from model.dataProviderFactory import DataStore
		myFactory = DataStore()
		myDataModel = myFactory.createDataProvider()
		myDataModel.putNewSurvey(request);
		return message_types.VoidMessage()



#try:
#	return TMP.items[request.name]
#except (IndexError, TypeError):
#	raise endpoints.NotFoundException('Greeting %s not found.' %
#		(request.name,))

	ID_RESOURCE = endpoints.ResourceContainer(
		message_types.VoidMessage,
		trainid=messages.StringField(1, variant=messages.Variant.STRING))
	@endpoints.method(ID_RESOURCE, Stats,
		path='stats/{trainid}', http_method='GET',
		name='getStats')
	def stats_list(self, request):
		from model.dataProviderFactory import DataStore
		myFactory = DataStore()
		myDataModel = myFactory.createDataProvider()
		stopList = myDataModel.findAllTrainStopById(request.trainid)
		dataTable = []
		stats = Stats()
		stats.stopList = StopCollection()
		for trainStop in stopList:
			weekDaySamples = trainStop.getDelayList(True, False)
			weekDayMed = trainStop.getMedianValue(weekDaySamples)

			festiveSamples = trainStop.getDelayList(False, True)
			festiveMed = trainStop.getMedianValue(festiveSamples)

			samples = trainStop.getDelayList(True, True)
			allMed = trainStop.getMedianValue(samples)

			dataTable.append([trainStop.name, weekDayMed, festiveMed])
			stats.stopList.items.append(
				Stop(
					stationName = trainStop.name,
					weekdayMedian = weekDayMed,
					festiveMedian = festiveMed,
					allMedian = trainStop.getMedianValue(samples),
					weekdaySamples = map(lambda delayCounter: delayCounter.delayInMinutes, weekDaySamples),
					weekdayCounters = map(lambda delayCounter: delayCounter.counter, weekDaySamples),
					festiveSamples = map(lambda delayCounter: delayCounter.delayInMinutes, festiveSamples),
					festiveCounters = map(lambda delayCounter: delayCounter.counter, festiveSamples),
					allSamples = map(lambda delayCounter: delayCounter.delayInMinutes, samples),
					allCounters = map(lambda delayCounter: delayCounter.counter, samples),
				))

		from view.formatter import toGMultiLineChartJSon
		stats.graphData = toGMultiLineChartJSon(dataTable)

		return stats
