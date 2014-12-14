import urllib
from s9 import S9
import datetime
import time

class DataProvider:
	""" This the product of an abstract factory """

	def RetrieveSourcePage(self):
		return ""

class OnLineData(DataProvider):
	url = ""

	def __init__(self, url="http://mobile.my-link.it/mylink/mobile/scheda?dettaglio=visualizza&numeroTreno=24114&codLocOrig=S01059&tipoRicerca=numero&lang=IT"):
		self.url = url

	def RetrieveSourcePage(self):
		#@todo manage HTTPException
		return urllib.urlopen(self.url).read()


class StoredData(DataProvider):

	def RetrieveSourcePage(self):
		""" use a NoSQL store """
		query = S9.query(S9.date==datetime.date.fromtimestamp(time.mktime(time.strptime("2014-12-14", "%Y-%m-%d"))))
		
		tmp = query.get()
		if tmp:
			return tmp.timings
		return ""

