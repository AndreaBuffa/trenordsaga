import urllib
from train import Train
from trainStop import TrainStop
from trainDescr import TrainDescr
from datetime import date

HTTP_URL = 'http://mobile.my-link.it/mylink/mobile/scheda?dettaglio=visualizza&numeroTreno='

class DataProvider:
	""" This the product of an abstract factory """

	def retrieveSourcePage(self, trainId):
		return ""

	def findAllTrainStopById(self, trainId):
		return ""

class OnLineData(DataProvider):
	url = ""

	def __init__(self):
		#codLocOrig=S01059&tipoRicerca=numero&lang=IT
		self.url = HTTP_URL

	def retrieveSourcePage(self, trainId, theDate):
		#@todo theDate
		self.url = self.url + trainId
		#@todo manage HTTPException
		return urllib.urlopen(self.url).read()


class StoredData(DataProvider):

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
		return TrainDescr.query().fetch()
