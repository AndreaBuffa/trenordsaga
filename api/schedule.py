import endpoints
from protorpc import messages
from protorpc import message_types
from protorpc import remote
from model.dataProviderFactory import DataStore
import utils.common
from utils.parser import ScheduleParser
from view.formatter import *
package = 'main_api'

class Stop(messages.Message):
	""" Stop class"""
	stationName = messages.StringField(1)
	expected_h = messages.IntegerField(2)
	expected_m = messages.IntegerField(3)
	real_h = messages.IntegerField(4)
	real_m = messages.IntegerField(5)
	certainty = messages.IntegerField(6)
	delay_m = messages.IntegerField(7)

class StopCollection(messages.Message):
	"""Collection of train Stop."""
	items = messages.MessageField(Stop, 1, repeated=True)

class DataSourceContainer(messages.Message):
	data = messages.StringField(1)

class SurveyGraphContainer(messages.Message):
	scheduled_real = messages.StringField(1)
	real_median = messages.StringField(2)

@endpoints.api(name='schedule', version='v1')
class ScheduleApi(remote.Service):
	"""Schedules API v1. Allows to query the time schedule of each train
	for a particular date"""

	ID_RESOURCE = endpoints.ResourceContainer(
		message_types.VoidMessage,
		trainid=messages.StringField(1, variant=messages.Variant.STRING),
		year=messages.StringField(2, variant=messages.Variant.STRING),
		month=messages.StringField(3, variant=messages.Variant.STRING),
		day=messages.StringField(4, variant=messages.Variant.STRING))

	#message_types.VoidMessage
	@endpoints.method(ID_RESOURCE, StopCollection,
	        path = 'train_stop_list/{trainid}/{year}/{month}/{day}',
	        http_method='GET', name = 'trains.listStop')
	def get_train_stop_list(self, request):
		ret = StopCollection();
		tmpDate = [];
		if not utils.common.buildDate(request.year, request.month,
		                              request.day, tmpDate):
		        return ret

		myFactory = DataStore()
		myDataModel = myFactory.createDataProvider()
		buffer = myDataModel.retrieveSourcePage(request.trainid,
		                                        tmpDate[0])

		if buffer:
			myParser = ScheduleParser(buffer)
			for schedule in myParser.GetTimings():
				ret.items.append(
				        Stop(stationName = schedule['name'],
				             expected_h = schedule['sched_h'],
				             expected_m = schedule['sched_m'],
				             real_h = schedule['real_h'],
				             real_m = schedule['real_m'],
				             certainty = schedule['certainty'],
				             delay_m = schedule['delay_m']))
		return ret


	@endpoints.method(ID_RESOURCE, DataSourceContainer,
	        path='train_data_source/{trainid}/{year}/{month}/{day}',
	        http_method='GET', name='trains.getDataSource')
	def get_train_data_source(self, request):
		ret = DataSourceContainer();
		tmpDate = [];
		if not utils.common.buildDate(request.year, request.month,
		                              request.day, tmpDate):
		        return ret

		myFactory = DataStore()
		myDataModel = myFactory.createDataProvider()
		ret.data = myDataModel.retrieveSourcePage(request.trainid,
		                                          tmpDate[0])
		return ret

	@endpoints.method(ID_RESOURCE, SurveyGraphContainer,
	        path='survey_graph_data/{trainid}/{year}/{month}/{day}',
	        http_method='GET', name='trains.getSurveyGraphData')
	def get_survey_graph_data(self, request):
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
			myFormatter = Formatter()
			ret.scheduled_real = myFormatter.ToLineChartJSon(survey)

			stops = myDataModel.findAllTrainStopById(request.trainid)
			delayDict = {}
			for trainStop in stops:
				delayDict[trainStop.name] = trainStop.getMedian(True, True)

			ret.real_median = myFormatter.ToColumnChartJSon(survey,
			                                                delayDict,
			                                                tmpDate[0])

		return ret

