from dataProvider import *

class DataProviderFactory:
	""" follows the abstract class patterns """
	def createDataProvider(self):
		return

class DataStore(DataProviderFactory):
	def createDataProvider(self):
		return GAEDatastore()
