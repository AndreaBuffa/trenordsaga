import urllib
from s9 import S9
from datetime import date
import datetime

class DataProvider:
	""" This the product of an abstract factory """

	def RetrieveSourcePage(self):
		return ""

class OnLineData(DataProvider):
	url = ""

	def __init__(self, url="http://mobile.my-link.it/mylink/mobile/scheda?dettaglio=visualizza&numeroTreno=24114"):
		self.url = url
	#codLocOrig=S01059&tipoRicerca=numero&lang=IT

	def RetrieveSourcePage(self):
		#@todo manage HTTPException
		return urllib.urlopen(self.url).read()


class StoredData(DataProvider):

	def RetrieveSourcePage(self, theDate):

		query = S9.query(S9.date==theDate)
		tmp = query.get()
		if tmp:
			return tmp.timings
		return ""
