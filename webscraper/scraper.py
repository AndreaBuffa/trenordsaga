import logging
from google.appengine.ext import deferred
from google.appengine.ext import db
from model.trainDescr import TrainDescr
from model.train import Train
from model.trainStop import *
import utils.common
import urllib
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

def get_train_list(url, fromStation, toStation, when, timeRange):

	#partenza=Lamezia+Terme+Centrale&arrivo=Catanzaro&giorno=27&mese=08&anno=2015&fascia=3&lang=IT
	#import cookielib, urllib2
	#cj = cookielib.CookieJar()
	#opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
	#r = opener.open("http://mobile.my-link.it/mylink/mobile/programmato")
	#r.read()
	#opener.addheaders = [('Origin', 'http://mobile.my-link.it'),
	#		     ('Referer', 'http://mobile.my-link.it/mylink/mobile/programmato?lang=IT'),
	#		     ('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'),
	#		     ('User-Agent', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.89 Safari/537.36'),
	#		    ]
	#r = opener.open("http://mobile.my-link.it/mylink/mobile/programmato", params)

	whenDate = datetime.fromtimestamp(mktime(time.strptime(when, "%Y-%m-%d")))
	if whenDate < datetime.now():
		return ""

	params = urllib.urlencode({'partenza': fromStation,
				   'arrivo': toStation,
				   'giorno': whenDate.day,
				   'mese': whenDate.month,
				   'anno': whenDate.year,
				   'fascia': timeRange,
				   'lang': 'IT'})
	f = urllib.urlopen(url, params)
	return f.read()

def get_train_details(url, hrefList):
	details = []
	for href in hrefList:
		req = urllib.urlopen(url + href)
		detailsContent = req.read()
		if detailsContent:
			details.append(detailsContent)
		#time.sleep(1)
	return details

