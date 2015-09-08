from train import Train
from trainStop import TrainStop
from trainDescr import TrainDescr
from service import Service

class DataProvider:
	""" This the product of an abstract factory """

	def retrieveSourcePage(self, trainId):
		return ""

	def findAllTrainStopById(self, trainId):
		return ""

	def findAllTrainDescr(self):
		return ""

	def findTrainDescrById(self, trainId):
		return ""

	def findAllTrainDescrByName(self, stationName):
		return

	def findAllTrainByMultipleId(self, keyList):
		return

	def getServiceURL(self, serviceName):
		return

class GAEDatastore(DataProvider):
	""" Use a Google App Engine Datastore """
	def retrieveSourcePage(self, trainId, theDate):
		query = Train.query(Train.trainId == trainId,
				Train.date == theDate)
		tmp = query.get()
		if tmp:
			return tmp.timings
		return ""

	def findAllTrainStopById(self, trainId):
		query = TrainStop.query(TrainStop.trainid == trainId)
		return query.fetch()

	def findAllTrainDescr(self):
		return TrainDescr.query().order(TrainDescr.type,
						TrainDescr.leaveStation,
						TrainDescr.leaveTime).fetch()

	def findTrainDescrById(self, trainId):
		return TrainDescr.query(TrainDescr.trainId == trainId).get()

	def findAllTrainDescrByName(self, stationName):
		results = []
		for tmp in TrainStop.query(TrainStop.name == stationName).fetch():
			result = self.findTrainDescrById(tmp.trainid)
			if result:
				results.append(result)
		return results

	def findAllTrainByMultipleId(self, keyList):
		ret = []
		for key in keyList:
			trainDescr = TrainDescr.query(
				TrainDescr.trainId == key).get()
			if trainDescr:
				ret.append(trainDescr)
		return ret

	def getServiceURL(self, serviceName):
		tmp = Service.query(Service.name == serviceName).get()
		if tmp:
			return tmp.URL
		return ""
