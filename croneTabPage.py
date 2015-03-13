''' some support routines '''

import webapp2
from model.dataProviderFactory import *
import model.s9
from model.trainStop import *
from view.scheduleParser import *
import datetime

def createTrainStop(timings, stops):
	for record in timings:
		myParser = ScheduleParser(record.timings)
		timeSchedule = myParser.GetTimings()
		for entry in timeSchedule:
			if not stops.has_key(entry['name']):
				station = TrainStop()
				station.name = entry['name']
				station.trainid = '24114'
				station.startdate = datetime.datetime.strptime('2014-12-18', "%Y-%m-%d")
				station.numofsurveys = 0
				station.delaysList = []
				stops[entry['name']] = station
			stops[entry['name']].numofsurveys += 1
			if entry['delay_m'] > 0:
				stops[entry['name']].updateDelayCounter(entry['delay_m'])
			stops[entry['name']].certainty = True if entry['certainty'] else False

class CroneTabPage(webapp2.RequestHandler):
	def get(self):
		self.response.headers['Content-Type'] = 'text/plain'
		self.response.write('Working...')
		myFactory = ChroneTab()
		myData = myFactory.createDataProvider()
		buffer = myData.RetrieveSourcePage()
		if buffer:
			timeSchedule = S9()
			timeSchedule.timings = buffer
			timeSchedule.put()
			stops = {}
			query = TrainStop.query(TrainStop.trainid == '24114')
			results = query.fetch()
			for record in results:
				stops[record.name] = record
			createTrainStop([timeSchedule], stops)
			for key, stop in stops.iteritems():
				stop.put()
		self.response.write('Done!')

app = webapp2.WSGIApplication([
    ('/batch', CroneTabPage),
], debug=True)


class Mean(webapp2.RequestHandler):
	def get(self, startDateString, endDateString, cmd):
		if startDateString and endDateString:
			try:
				startDate = datetime.datetime.strptime(startDateString, "%Y-%m-%d").date()
				endDate = datetime.datetime.strptime(endDateString, "%Y-%m-%d").date()
			except ValueError:
				self.response.headers['Content-Type'] = 'text/plain'
				self.response.write('Invalid dates')
				return
			self.response.write('Computing Mean, working...')
			#delete accumulators
			stops = {}
			if cmd == 'reset':
				trainstops = TrainStop.query(TrainStop.trainid == '24114')
				ndb.delete_multi([key for key in trainstops.iter(keys_only = True)])
			else:
				query = TrainStop.query(TrainStop.trainid == '24114')
				results = query.fetch()
				for record in results:
					stops[record.name] = record
			#create new ones
			timings = S9.query(ndb.AND(S9.date >= startDate,
									S9.date <= endDate)).fetch()
			createTrainStop(timings, stops)
			for key, stop in stops.iteritems():
				stop.put()
			self.response.write(datetime.datetime.now())

mean = webapp2.WSGIApplication([
	(r'/mean/(\d{4}-\d{1,2}-\d{1,2})/(\d{4}-\d{1,2}-\d{1,2})/(reset)*', Mean)
], debug=True)
