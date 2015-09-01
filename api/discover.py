import endpoints
from protorpc import messages
from protorpc import message_types
from protorpc import remote
from model.dataProviderFactory import DataStore
import webscraper.scraper
import utils.parser
package = 'main_api'

class Train(messages.Message):
	""" Surveyed train class"""
	trainId = messages.StringField(1)
	type = messages.StringField(2)
	leaveStation = messages.StringField(3)
	endStation = messages.StringField(4)
	arriveTime = messages.StringField(5)
	leaveTime = messages.StringField(6)
	surveyedFrom = messages.StringField(7)

class TrainList(messages.Message):
	"""Collection of train objects"""
	items = messages.MessageField(Train, 1, repeated=True)

class StationTrain(messages.Message):
	key = messages.StringField(1)
	type = messages.StringField(2)
	leaveStation = messages.StringField(3)
	endStation = messages.StringField(4)
	arriveTime = messages.StringField(5)
	leaveTime = messages.StringField(6)
	surveyedFrom = messages.StringField(7)
	isSurveyed = messages.BooleanField(8)

class StationTrainList(messages.Message):
	"""Collection of train objects"""
	items = messages.MessageField(StationTrain, 1, repeated=True)

class TrainKeyParam(messages.Message):
	key = messages.StringField(1)

class MultipleTrainKeyRequest(messages.Message):
	keyList = messages.MessageField(TrainKeyParam, 1, repeated=True)

@endpoints.api(name='discover', version='v1')
class DicoverApi(remote.Service):
	"""Discover API v1. Retrieve wichich train number and lines are
	managed by TrenordSaga"""

	ID_RESOURCE = endpoints.ResourceContainer(
		message_types.VoidMessage)
	@endpoints.method(ID_RESOURCE, TrainList,
		path='surveyed_train_list', http_method='GET',
		name='trains.listSurveyedTrain')
	def get_surveyed_collection(self, request):
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
				surveyedFrom = str(trainDescr.date)))

		return ret


	@endpoints.method(MultipleTrainKeyRequest,
		TrainList,
		http_method='POST',
		name='trains.surveyedTrainByIdList')
	def check_surveyed(self, request):
		myFactory = DataStore()
		myDataModel = myFactory.createDataProvider()
		trainDescrList = TrainList()
		for trainDescr in myDataModel.findAllTrainByMultipleId(
			[ keyItem.key for keyItem in request.keyList ]):
			trainDescrList.items.append(Train(
					trainId = trainDescr.trainId,
					type = trainDescr.type,
					leaveStation = trainDescr.leaveStation,
					endStation = trainDescr.endStation,
					arriveTime = trainDescr.arriveTime,
					leaveTime = trainDescr.leaveTime,
					surveyedFrom = str(trainDescr.date)))
		return trainDescrList


	ID_RESOURCE = endpoints.ResourceContainer(
		message_types.VoidMessage,
		fromStation=messages.StringField(1, variant=messages.Variant.STRING),
		toStation=messages.StringField(2, variant=messages.Variant.STRING),
		when=messages.StringField(3, variant=messages.Variant.STRING),
		timeRange=messages.StringField(4, variant=messages.Variant.STRING))

	@endpoints.method(ID_RESOURCE, StationTrainList,
		path='search_from_to/{fromStation}/{toStation}/{when}/{timeRange}', http_method='GET',
		name='trains.searchFromTo')
	def search_from_to(self, request):
		#@todo validate when and time range
		myFactory = DataStore()
		myDataModel = myFactory.createDataProvider()
		# query a third-party server
                serviceURL = myDataModel.getServiceURL('TrainListByStation')
		trainListString = webscraper.scraper.get_train_list(serviceURL,
							request.fromStation,
							request.toStation,
							request.when,
							request.timeRange)

		hrefList = utils.parser.extract_links(trainListString)
		trainList = webscraper.scraper.get_train_details(serviceURL,
								 hrefList)

		detailsList = utils.parser.extract_train_details(trainList)

		trainDescrList = StationTrainList()
		for train in detailsList:
			trainDescr = myDataModel.findTrainDescrById(train['id'])
			trainDescrList.items.append(StationTrain(
					key = trainDescr.trainId,
					type = trainDescr.type,
					leaveStation = trainDescr.leaveStation,
					endStation = trainDescr.endStation,
					arriveTime = trainDescr.arriveTime,
					leaveTime = trainDescr.leaveTime,
					surveyedFrom = str(trainDescr.date)))
		return trainDescrList
