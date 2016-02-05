import endpoints
from protorpc import messages
from protorpc import message_types
from protorpc import remote
from model.dataProviderFactory import DataStore
package = 'main_api'

class Stop(messages.Message):
	""" Stop class"""
	stationName = messages.StringField(1)
	weekdayMedian = messages.FloatField(2)
	festiveMedian = messages.FloatField(3)
	allMedian = messages.FloatField(4)

class StopCollection(messages.Message):
	"""Collection of train Stop."""
	items = messages.MessageField(Stop, 1, repeated=True)

class Stats(messages.Message):
	graphData = messages.StringField(1)
	stopList = messages.MessageField(StopCollection, 2)


@endpoints.api(name='statistics', version='v1')
class StatisticsApi(remote.Service):
	"""Statistics API v1. Retrieve statistics such as median delay for
	a particular train line or station."""

	ID_RESOURCE = endpoints.ResourceContainer(
		message_types.VoidMessage,
		trainid=messages.StringField(1, variant=messages.Variant.STRING),
		dayFilter=messages.StringField(2, variant=messages.Variant.STRING))
	@endpoints.method(ID_RESOURCE, StopCollection,
		path='train_stop_list/{trainid}/{dayFilter}', http_method='GET',
		name='trains.listStop')
	def stop_list(self, request):
		myFactory = DataStore()
		myDataModel = myFactory.createDataProvider()
		results = myDataModel.findAllTrainStopById(request.trainid)
		ret = StopCollection()
		if request.dayFilter == "dayOff":
			dayOff = True
			workDay = False
		elif request.dayFilter == "workDay":
			dayOff = False
			workDay = True
		elif request.dayFilter == "all":
			dayOff = True
			workDay = True
		else:
			return ret
		for trainStop in results:
			ret.items.append(Stop(stationName = trainStop.name,
                                  median = trainStop.getMedian(workDay, dayOff)))
		return ret

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
		name='trains.getStats')
	def stats_list(self, request):
		from view.formatter import *
		myFactory = DataStore()
		myDataModel = myFactory.createDataProvider()
		stopList = myDataModel.findAllTrainStopById(request.trainid)
		dataTable = []
		stats = Stats()
		stats.stopList = StopCollection()
		for trainStop in stopList:
			weekDayMed = trainStop.getMedian(True, False)
			festiveMed = trainStop.getMedian(False, True)
			allMed = trainStop.getMedian(True, True)
			dataTable.append([trainStop.name, weekDayMed, festiveMed, allMed])
			stats.stopList.items.append(
				Stop(
					stationName = trainStop.name,
					weekdayMedian = weekDayMed,
					festiveMedian = festiveMed,
					allMedian = allMed
				))

		myFormatter = Formatter()
		stats.graphData = myFormatter.ToGMultiLineChartJSon(dataTable)

		return stats
