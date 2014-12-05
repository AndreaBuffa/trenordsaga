from dataProvider import *

class DataProviderFactory: 
	""" follows the abstract class patterns """
	def createDataProvider(self):
		return

class ChroneTab(DataProviderFactory):
	def createDataProvider(self):
		return OnLineData()

class Validator(DataProviderFactory):
	def createDataProvider(self):
		return StoredData()

