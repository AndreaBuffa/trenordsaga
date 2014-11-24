class DataProvider:
	""" This the product of an abstract factory """

	def RetrieveDelayTimeline(self):
		return ""

	def RetrieveSourcePage(self):
		return ""

class OnLineData(DataProvider):
	url = ""

	def __init__(self, url): 
		self.url = url

	def RetrieveDelayTimeline(self):
		return ""

	def RetrieveSourcePage(self):
		return urllib.urlopen(url).read()


class StoredData(DataProvider):

	def RetrieveDelayTimeline(self):
		""" use a NoSQL datastore """

	def RetrieveSourcePage(self):
		""" use an bject store """
