import logging
from google.appengine.ext import deferred
from google.appengine.ext import db

from model.dataProviderFactory import *
import model.s9
from model.trainStop import *
from view.scheduleParser import *
import common

BATCH_SIZE = 30  # ideal batch size may vary based on entity size.

def Mean(cursor=None, num_updated=0):
    stops = {}
    query = S9.query()
    if cursor:
        query = TrainStop.query(TrainStop.trainid == '24114')
        results = query.fetch()
        for record in results:
            stops[record.name] = record
        query.with_cursor(cursor)
    else:
        trainstops = TrainStop.query(TrainStop.trainid == '24114')
        ndb.delete_multi([key for key in trainstops.iter(keys_only = True)])

    timings = query.fetch(limit=BATCH_SIZE)
    if len(timings):
        common.createTrainStop(timings, stops)
        for key, stop in stops.iteritems():
            stop.put()
        num_updated += len(timings)
        deferred.defer(Mean, cursor=query.iter(), num_updated=num_updated)
    else:
        logging.debug('Mediana computation complete with %d updates!', num_updated)


