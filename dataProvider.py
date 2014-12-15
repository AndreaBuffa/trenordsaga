import urllib
from s9 import S9
from datetime import date

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
		#time.strptime("2014-12-15", "%Y-%m-%d")
		query = S9.query(S9.date==date.today())
		
		tmp = query.get()
		if tmp:
			return tmp.timings
		return ""

