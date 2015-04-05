import urllib
from train import Train
from datetime import date

HTTP_URL = 'http://mobile.my-link.it/mylink/mobile/scheda?dettaglio=visualizza&numeroTreno='

class DataProvider:
	""" This the product of an abstract factory """
	trainId = 0

	def __init__(self, trainId):
		self.url = url
	#codLocOrig=S01059&tipoRicerca=numero&lang=IT

	def RetrieveSourcePage(self):
		return ""

class OnLineData(DataProvider):
	url = ""

	def __init__(self, trainId = '24114'):
		self.url = HTTP_URL + trainId
	#codLocOrig=S01059&tipoRicerca=numero&lang=IT

	def RetrieveSourcePage(self):
		#@todo manage HTTPException
		return urllib.urlopen(self.url).read()


class StoredData(DataProvider):

	def __init__(self, trainId = '24114'):
		self.trainId = trainId

	def RetrieveSourcePage(self, theDate):

		query = Train.query(Train.trainId == self.trainId, Train.date == theDate)
		tmp = query.get()
		if tmp:
			return tmp.timings
		return ""

