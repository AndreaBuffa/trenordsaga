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

def retrieve_schedule(trainId, attemps=MAX_ATTEMPS):
	trainDescr = TrainDescr.query(TrainDescr.trainId == trainId).get()
	if not trainDescr:
		logging.debug('retrieve_schedule: cannot retrieve Train Descriptor %s!',
			trainId)
		return

	trainExist = Train.query(Train.trainId == trainId,
		Train.date == datetime.datetime.today()).get()

	if trainExist:
		logging.debug('retrieve_schedule: Train %s already stored!',
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
				deferred.defer(retrieve_schedule, trainId,
					       attemps=attemps-1)
			else:
				logging.debug('retrieve_schedule: %d attemps failed for train %s !',
					      MAX_ATTEMPS, trainId)

def scrape_train_List(url, fromStation, toStation):

	#partenza=Lamezia+Terme+Centrale&arrivo=Catanzaro&giorno=27&mese=08&anno=2015&fascia=3&lang=IT
	params = urllib.urlencode({'stazione': fromStation,
				   'arrivo': toStation,
				   'giorno': '27',
				   'mese': '08',
				   'anno': '27',
				   'fascia': '3',
				   'lang': 'IT'})
	f = urllib.urlopen(url, params)
	return f.read()

