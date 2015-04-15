from dataProvider import *

class DataProviderFactory:
	""" follows the abstract class patterns """
	def createDataProvider(self):
		return

class CronTab(DataProviderFactory):
	def createDataProvider(self):
		return OnLineData()

class Validator(DataProviderFactory):
	def createDataProvider(self):
		return StoredData()

class FrontEnd(DataProviderFactory):
	def createDataProvider(self):
		return StoredData()

class DataStore(DataProviderFactory):
	def createDataProvider(self):
		return StoredData()
