import logging
from google.appengine.ext import deferred
from google.appengine.ext import db

from model.dataProviderFactory import *
from model.s9 import S9
from model.train import Train
from model.trainDescr import TrainDescr
import common

BATCH_SIZE = 30  # ideal batch size

def Migrate(cursor=None, num_updated=0):
	stops = {}
	queryAllS9 = S9.query().order(S9.date)
	if cursor:
		timings, cursor, more = queryAllS9.fetch_page(BATCH_SIZE, start_cursor=cursor)
	else:
		timings, cursor, more = queryAllS9.fetch_page(BATCH_SIZE)

	if len(timings):
		for record in timings:
			timeSchedule = Train()
			timeSchedule.timings = record.timings
			timeSchedule.trainId = record.trainId
			timeSchedule.date = record.date
			timeSchedule.put()
		num_updated += len(timings)
	if more:
		deferred.defer(Migrate, cursor=cursor, num_updated=num_updated)
		logging.debug('Computed %d updates!', num_updated)
	else:
		logging.debug('Migration complete with %d updates!', num_updated)

def AddStatus(cursor=None, num_updated=0):
	queryAll = TrainDescr.query()
	if cursor:
		records, cursor, more = queryAll.fetch_page(BATCH_SIZE, start_cursor=cursor)
	else:
		records, cursor, more = queryAll.fetch_page(BATCH_SIZE)

	if len(records):
		for record in records:
			if not record.status:
				record.status = 'enabled'
				record.put()
		num_updated += len(records)
	if more:
		deferred.defer(AddStatus, cursor=cursor, num_updated=num_updated)
		logging.debug('Status migration... Computed %d updates!', num_updated)
	else:
		logging.debug('Status Migration complete with %d updates!', num_updated)
