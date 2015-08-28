import webapp2
import mean
import entityMigration
from google.appengine.ext import deferred
import webscraper.scraper
from model.trainDescr import TrainDescr

class BatchHandler(webapp2.RequestHandler):
	def get(self, task):
		msg = b''
		if task == 'mean':
			deferred.defer(mean.Mean)
			msg = 'Mediana computation successfully initiated.'

		elif task == 'migrate':
			deferred.defer(entityMigration.Migrate)
			msg = 'Schema migration successfully initiated.'

		elif task == 'retrieve':
			for train in TrainDescr.query().fetch():
				deferred.defer(webscraper.scraper.retrieve_schedule, train.trainId)
			msg = 'Web scraping successfully initiated.'
		else:
			msg = 'Failed, not existing task'

		self.response.out.write('Starting job....' + msg)

batchJob = webapp2.WSGIApplication([(r'/batch/([a-z]+)', BatchHandler)])
