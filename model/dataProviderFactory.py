from dataProvider import *

class DataProviderFactory:
	""" follows the abstract class patterns """
	def createDataProvider(self):
		return

class CronTab(DataProviderFactory):
	def createDataProvider(self, trainId='24114'):
		return OnLineData(trainId)

class Validator(DataProviderFactory):
	def createDataProvider(self, trainId='24114'):
		return StoredData(trainId)

class FrontEnd(DataProviderFactory):
	def createDataProvider(self, trainId='24114'):
		return StoredData(trainId)

