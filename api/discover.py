import endpoints
from protorpc import messages
from protorpc import message_types
from protorpc import remote
from model.dataProviderFactory import DataStore
from webscraper.scraper import *
from utils.parser import *
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
		toStation=messages.StringField(2, variant=messages.Variant.STRING))
	@endpoints.method(ID_RESOURCE, StationTrainList,
		path='get_train_list_by_name/{fromStation}/{toStation}', http_method='GET',
		name='trains.getTrainListByName')
	def get_train_by_station_name(self, request):
		myFactory = DataStore()
		myDataModel = myFactory.createDataProvider()

		'''
		from model.service import Service
		tmp = Service()
		tmp.name = 'TrainListByStation'
		tmp.URL = 'http://mobile.my-link.it/mylink/mobile/stazione'
		tmp.decription = "suca"
		tmp.put()
		'''
		trainListString = scrape_train_List(
				myDataModel.getServiceURL('TrainListByStation'),
				request.fromStation,
				request.toStation)

		trainDescrList = StationTrainList()
		for trainDescr in myDataModel.findAllTrainDescrByName(request.fromStation):
			trainDescrList.items.append(StationTrain(
					key = trainDescr.trainId,
					type = trainDescr.type,
					leaveStation = trainDescr.leaveStation,
					endStation = trainDescr.endStation,
					arriveTime = trainDescr.arriveTime,
					leaveTime = trainDescr.leaveTime,
					surveyedFrom = str(trainDescr.date)))
		return trainDescrList
