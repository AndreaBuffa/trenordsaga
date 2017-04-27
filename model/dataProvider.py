
class DataProvider:
	""" This the product of an abstract factory """

	def retrieveSourcePage(self, trainId):
		raise NotImplementedError

	def findAllTrainStopById(self, trainId):
		raise NotImplementedError

	def findAllTrainDescr(self):
		raise NotImplementedError

	def findTrainDescrById(self, trainId):
		raise NotImplementedError

	def findAllTrainDescrByName(self, stationName):
		raise NotImplementedError

	def findAllTrainByMultipleId(self, keyList):
		raise NotImplementedError

	def getServiceURL(self, serviceName):
		raise NotImplementedError

	def putNewSurvey(self, survey):
		raise NotImplementedError

	def getNewSurvey(self):
		raise NotImplementedError

class GAEDatastore(DataProvider):
	""" Use a Google App Engine Datastore """
	def retrieveSourcePage(self, trainId, theDate):
		from train import Train
		query = Train.query(Train.trainId == trainId,
				Train.date == theDate)
		tmp = query.get()
		if tmp:
			return tmp.timings
		return ""

	def findAllTrainStopById(self, trainId):
		from trainStop import TrainStop
		query = TrainStop.query(TrainStop.trainid == trainId).order(TrainStop.index)
		return query.fetch()

	def findAllTrainDescr(self):
		from trainDescr import TrainDescr
		return TrainDescr.query(TrainDescr.status == 'enabled').order(TrainDescr.type,
						TrainDescr.leaveStation,
						TrainDescr.leaveTime).fetch()

	def findTrainDescrById(self, trainId):
		from trainDescr import TrainDescr
		return TrainDescr.query(TrainDescr.trainId == trainId).get()

	def findAllTrainDescrByName(self, stationName):
		from trainStop import TrainStop
		results = []
		for tmp in TrainStop.query(TrainStop.name == stationName).fetch():
			result = self.findTrainDescrById(tmp.trainid)
			if result:
				results.append(result)
		return results

	def findAllTrainByMultipleId(self, keyList):
		from trainDescr import TrainDescr
		ret = []
		for key in keyList:
			trainDescr = TrainDescr.query(
				TrainDescr.trainId == key).get()
			if trainDescr:
				ret.append(trainDescr)
		return ret

	def getServiceURL(self, serviceName):
		from service import Service
		tmp = Service.query(Service.name == serviceName).get()
		if tmp:
			return tmp.URL
		return ""

	def putNewSurvey(self, survey):
		from trainDescr import TrainDescr
		trainDescrRec = TrainDescr()
		trainDescrRec.trainId = survey.num
		trainDescrRec.type = survey.trainType
		trainDescrRec.leaveStation = survey.fromStation
		trainDescrRec.endStation = survey.to
		trainDescrRec.arriveTime = survey.arrive
		trainDescrRec.leaveTime = survey.leave
		#trainDescrRec.date =
		trainDescrRec.status = 'disabled'
		trainDescrRec.put()
		return True;

	def getNewSurvey(self):
		from trainDescr import TrainDescr
		return TrainDescr.query(TrainDescr.status == 'disabled').fetch();
