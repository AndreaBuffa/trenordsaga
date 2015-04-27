import endpoints
from protorpc import messages
from protorpc import message_types
from protorpc import remote
from model.dataProviderFactory import DataStore
package = 'main_api'

class SurveyedTrain(messages.Message):
	""" Surveyed train class"""
	trainId = messages.StringField(1)
	type = messages.StringField(2)
	leaveStation = messages.StringField(3)
	endStation = messages.StringField(4)
	arriveTime = messages.StringField(5)
	leaveTime = messages.StringField(6)
	surveyedFrom = messages.StringField(7)

class SurveyedTrainColl(messages.Message):
	"""Collection of surveyed trains."""
	items = messages.MessageField(SurveyedTrain, 1, repeated=True)


@endpoints.api(name='discover', version='v1')
class DicoverApi(remote.Service):
	"""Discover API v1. Retrieve wichich train number and lines are
	managed by TrenordSaga"""

	ID_RESOURCE = endpoints.ResourceContainer(
		message_types.VoidMessage)
	@endpoints.method(ID_RESOURCE, SurveyedTrainColl,
		path='surveyed_train_list', http_method='GET',
		name='trains.listSurveyedTrain')
	def get_surveyed_collection(self, request):
		myFactory = DataStore()
		myDataModel = myFactory.createDataProvider()
		ret = SurveyedTrainColl()
		for trainDescr in myDataModel.findAllTrainDescr():
			ret.items.append(SurveyedTrain(trainId = trainDescr.trainId,
				type = trainDescr.type,
				leaveStation = trainDescr.leaveStation,
				endStation = trainDescr.endStation,
				arriveTime = trainDescr.arriveTime,
				leaveTime = trainDescr.leaveTime,
				surveyedFrom = str(trainDescr.date)))

		return ret
