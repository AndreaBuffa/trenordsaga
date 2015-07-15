from train import Train
from trainStop import TrainStop
from trainDescr import TrainDescr

class DataProvider:
	""" This the product of an abstract factory """

	def retrieveSourcePage(self, trainId):
		return ""

	def findAllTrainStopById(self, trainId):
		return ""

	def findAllTrainDescr(self):
		return ""

class GAEDatastore(DataProvider):
	""" Use a Google App Engine Datastore """
	def retrieveSourcePage(self, trainId, theDate):
		query = Train.query(Train.trainId == trainId, Train.date == theDate)
		tmp = query.get()
		if tmp:
			return tmp.timings
		return ""

	def findAllTrainStopById(self, trainId):
		query = TrainStop.query(TrainStop.trainid == trainId)
		return query.fetch()

	def findAllTrainDescr(self):
		return TrainDescr.query().order(TrainDescr.type).fetch()

	def findTrainDescrById(self, trainId):
		return TrainDescr.query(TrainDescr.trainId == trainId).get()
