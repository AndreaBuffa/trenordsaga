import webapp2
import mean
import entityMigration
from google.appengine.ext import deferred
import webscraper.scraper
from model.trainDescr import TrainDescr
#import datetime

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
			'''
			tmp = TrainDescr()
			tmp.trainId = '23222'
			tmp.type = 'S3'
			#tmp.url = 'http://mobile.my-link.it/mylink/mobile/scheda?dettaglio=visualizza&numeroTreno=24114&codLocOrig=S01059&tipoRicerca=numero&lang=IT'
			tmp.url = 'http://mobile.my-link.it/mylink/mobile/scheda?dettaglio=visualizza&numeroTreno=23222&codLocOrig=S01825&tipoRicerca=numero&lang=IT'
			tmp.leaveStation = "Bobo"
			tmp.endStation = "Ballo"
			tmp.arriveTime = "09:54"
			tmp.leaveTime = "08:08"
			tmp.date = datetime.datetime.today()
			tmp.put()
			'''
			for train in TrainDescr.query().fetch():
				print train.trainId
				deferred.defer(webscraper.scraper.Scraper, train.trainId)
			msg = 'Web scraping successfully initiated.'
		else:
			msg = 'Failed, not existing task'
		self.response.out.write('Starting job....' + msg)

batchJob = webapp2.WSGIApplication([(r'/batch/([a-z]+)', BatchHandler)])
