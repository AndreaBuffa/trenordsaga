import logging
from google.appengine.ext import deferred
from google.appengine.ext import db
from model.trainDescr import TrainDescr
from model.train import Train
from model.trainStop import *
import utils.common
import urllib
import cookielib, urllib2
from datetime import datetime
from time import mktime
import time

MAX_ATTEMPS = 3

def retrieve_schedule(trainId, attemps=MAX_ATTEMPS):

	trainDescr = TrainDescr.query(TrainDescr.trainId == trainId).get()
	if not trainDescr:
		logging.debug('retrieve_schedule: cannot retrieve Train Descriptor %s!',
			trainId)
		return

	trainExist = Train.query(Train.trainId == trainId,
		Train.date == datetime.today()).get()

	if trainExist:
		logging.debug('retrieve_schedule: Train %s already stored!',
			trainDescr.trainId)
	else:
		try:
			if not trainDescr.url:
				logging.debug('retrieve_schedule: trainId %s with no URL!',
							trainId)
				return
			source = urllib.urlopen(trainDescr.url)
			pageBuffer = source.read()
			#@todo source.getcode() ?
			timeSchedule = Train()
			timeSchedule.timings = pageBuffer
			timeSchedule.trainId = trainDescr.trainId
			timeSchedule.date = datetime.today()
			timeSchedule.put()

			stops = {}
			query = TrainStop.query(TrainStop.trainid == trainId)
			results = query.fetch()
			for record in results:
				stops[record.name] = record

			utils.common.createTrainStop(timeSchedule, stops)
			for key, stop in stops.iteritems():
				stop.put()
		except IOError:
			# retry if the server does not respond. 
			# @todo Sleep before trying again?
			if attemps > 0:
				deferred.defer(retrieve_schedule, trainId,
					       attemps=attemps-1)
			else:
				logging.debug('retrieve_schedule: %s attemps failed for train %s !',
					      MAX_ATTEMPS, trainId)

def get_http_opener():
	cj = cookielib.CookieJar()
	opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
	return opener

def get_train_list(opener, url, fromStation, toStation, when, timeRange):
	try:
		whenDate = datetime.fromtimestamp(
					mktime(time.strptime(when, "%Y-%m-%d")))
	except ValueError:
		logging.debug('get_train_list: invalid date format')
		return ""

	if whenDate.date() < datetime.now().date():
		logging.debug('get_train_list: invalid date')
		return ""

	params = urllib.urlencode({'partenza': fromStation,
				   'arrivo': toStation,
				   'giorno': whenDate.day,
				   'mese': whenDate.month,
				   'anno': whenDate.year,
				   'fascia': timeRange,
				   'lang': 'IT'})

	r = opener.open(url, params)

	return r.read()

def get_train_details(opener, url, hrefList):
	details = []
	if not opener:
		logging.debug('get_train_details: opener is None!')
		return details
	for href in hrefList:
		req = opener.open(url + href)
		detailsContent = req.read()
		if detailsContent:
			details.append(detailsContent)
	return details

