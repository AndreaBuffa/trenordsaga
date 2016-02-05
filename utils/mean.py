import logging
from google.appengine.ext import deferred
from google.appengine.ext import db

from model.dataProviderFactory import *
import model.s9
from model.trainStop import *
from parser import ScheduleParser
import common

BATCH_SIZE = 30  # ideal batch size

def Mean(cursor=None, num_updated=0):
	stops = {}
	queryTimeSchedules = S9.query().order(S9.date)
	if cursor:
		query = TrainStop.query(TrainStop.trainid == '24114')
		results = query.fetch()
		for record in results:
			stops[record.name] = record
		timings, cursor, more = queryTimeSchedules.fetch_page(BATCH_SIZE, start_cursor=cursor)
	else:
		trainstops = TrainStop.query(TrainStop.trainid == '24114')
		ndb.delete_multi([key for key in trainstops.iter(keys_only = True)])
		timings, cursor, more = queryTimeSchedules.fetch_page(BATCH_SIZE)

	if len(timings):
		for record in timings:
			common.createTrainStop(record, stops)
			for key, stop in stops.iteritems():
				stop.put()
		num_updated += len(timings)
		deferred.defer(Mean, cursor=cursor, num_updated=num_updated)
		logging.debug('Computed %d updates!', num_updated)
	else:
		logging.debug('Mediana computation complete with %d updates!', num_updated)
