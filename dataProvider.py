import urllib

class DataProvider:
	""" This the product of an abstract factory """

	def RetrieveDelayTimeline(self):
		return ""

	def RetrieveSourcePage(self):
		return ""

class OnLineData(DataProvider):
	url = ""

	def __init__(self, url="http://mobile.my-link.it/mylink/mobile/scheda?dettaglio=visualizza&numeroTreno=24108&codLocOrig=S01059&tipoRicerca=numero&lang=IT"): 
		self.url = url

	def RetrieveDelayTimeline(self):
		return ""

	def RetrieveSourcePage(self):
		return urllib.urlopen(self.url).read()


class StoredData(DataProvider):

	def RetrieveDelayTimeline(self):
		""" use a NoSQL datastore """

	def RetrieveSourcePage(self):
		""" use an bject store """
