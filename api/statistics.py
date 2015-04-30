import endpoints
from protorpc import messages
from protorpc import message_types
from protorpc import remote
from model.dataProviderFactory import DataStore
package = 'main_api'

class Stop(messages.Message):
	""" Stop class"""
	stationName = messages.StringField(1)
	median = messages.FloatField(2)


class StopCollection(messages.Message):
	"""Collection of train Stop."""
	items = messages.MessageField(Stop, 1, repeated=True)


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
			ret.items.append(Stop(stationName=trainStop.name,
				median=trainStop.getMedian(workDay, dayOff)))
		return ret

	NAME_RESOURCE = endpoints.ResourceContainer(
		message_types.VoidMessage,
		name=messages.StringField(1, variant=messages.Variant.STRING))
	@endpoints.method(NAME_RESOURCE, Stop,
					path='train_stop_get/{name}', http_method='GET',
					name='trains.getStop')
	def stop_get(self, request):
		pass
		#try:
		#	return TMP.items[request.name]
		#except (IndexError, TypeError):
		#	raise endpoints.NotFoundException('Greeting %s not found.' %
		#		(request.name,))
