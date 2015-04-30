import logging
from google.appengine.ext import deferred
from google.appengine.ext import db
from model.trainDescr import TrainDescr
from model.train import Train
from model.trainStop import *
import utils.common
import urllib
import datetime

MAX_ATTEMPS = 3

def Scraper(trainId, attemps=MAX_ATTEMPS):
	trainDescr = TrainDescr.query(TrainDescr.trainId == trainId).get()
	if not trainDescr:
		logging.debug('SCRAPER: cannot retrieve Train Descriptor %s!',
			trainId)
		return

	trainExist = Train.query(Train.trainId == trainId,
		Train.date == datetime.datetime.today()).get()

	if trainExist:
		logging.debug('SCRAPER: Train %s already stored!',
			trainDescr.trainId)
	else:
		try:
			source = urllib.urlopen(trainDescr.url)
			pageBuffer = source.read()
			#@todo source.getcode() ?
			timeSchedule = Train()
			timeSchedule.timings = pageBuffer
			timeSchedule.trainId = trainDescr.trainId
			timeSchedule.date = datetime.datetime.today()
			timeSchedule.put()

			stops = {}
			query = TrainStop.query(TrainStop.trainid == trainId)
			results = query.fetch()
			for record in results:
				stops[record.name] = record
			utils.common.createTrainStop([timeSchedule], stops)
			for key, stop in stops.iteritems():
				stop.put()
		except IOError:
			# retry if the server does not respond. 
			# @todo Sleep before trying again?
			if attemps > 0:
				deferred.defer(Scraper,	trainId, attemps=attemps-1)
			else:
				logging.debug('SCRAPER: %d attemps failed for train %s !',
					MAX_ATTEMPS, trainId)

