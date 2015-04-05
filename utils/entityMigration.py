import logging
from google.appengine.ext import deferred
from google.appengine.ext import db

from model.dataProviderFactory import *
from model.s9 import S9
from model.train import Train
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
