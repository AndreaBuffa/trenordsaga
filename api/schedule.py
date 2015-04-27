import endpoints
from protorpc import messages
from protorpc import message_types
from protorpc import remote
from model.dataProviderFactory import DataStore
from datetime import datetime
from view.scheduleParser import *
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
		path='train_stop_list/{trainid}/{year}/{month}/{day}', http_method='GET',
		name='trains.listStop')
	def get_train_stop_list(self, request):
		myFactory = DataStore()
		myDataModel = myFactory.createDataProvider()
		ret = StopCollection();
		if request.year and request.month and request.day:
			try:
				theDate = datetime.strptime(request.year+"-"+request.month+"-"+request.day, "%Y-%m-%d").date()
			except ValueError:
				return ret
		else:
			return ret
		buffer = myDataModel.retrieveSourcePage(request.trainid, theDate)
		if buffer:
			myParser = ScheduleParser(buffer)
			for schedule in myParser.GetTimings():
				ret.items.append(Stop(stationName = schedule['name'],
					expected_h = schedule['sched_h'],
					expected_m = schedule['sched_m'],
					real_h = schedule['real_h'],
					real_m = schedule['real_m'],
					certainty = schedule['certainty'],
					delay_m = schedule['delay_m']))
		return ret
