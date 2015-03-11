import webapp2
from model.dataProviderFactory import *
import model.s9
from model.trainStop import *
from view.scheduleParser import *
import datetime

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
			myParser = ScheduleParser(buffer)
			timeSchedule = myParser.GetTimings()
			for entry in timeSchedule:
				query = TrainStop.query(ndb.AND(TrainStop.name == entry['name'],
												TrainStop.trainid == '24114'))
				station = query.get()
				if not station:
						station = TrainStop()
						station.name = entry['name']
						station.trainid = '24114'
						station.startdate = datetime.datetime.strptime('2014-12-18', "%Y-%m-%d")
						station.numofsurveys = 0
						station.delay = 0
				station.numofsurveys += 1
				if entry['delay_m'] > 0:
						station.delay += entry['delay_m']
				station.certainty = True if entry['certainty'] else False
				station.put()

		self.response.write('Done!')

app = webapp2.WSGIApplication([
    ('/batch', CroneTabPage),
], debug=True)


class Mean(webapp2.RequestHandler):
	def get(self):
		self.response.headers['Content-Type'] = 'text/plain'
		self.response.write('Computing Mean, working...')
		#delete accumulators
		trainstops = TrainStop.query(TrainStop.trainid == '24114')
		ndb.delete_multi([key for key in trainstops.iter(keys_only = True)])
		#create new ones
		timings = S9.query().fetch()
		for record in timings:
				myParser = ScheduleParser(record.timings)
				timeSchedule = myParser.GetTimings()
				for entry in timeSchedule:
					query = TrainStop.query(ndb.AND(TrainStop.name == entry['name'],
												TrainStop.trainid == '24114'))
					station = query.get()
					if not station:
						station = TrainStop()
						station.name = entry['name']
						station.trainid = '24114'
						station.startdate = datetime.datetime.strptime('2014-12-18', "%Y-%m-%d")
						station.numofsurveys = 0
						station.delay = 0
					station.numofsurveys += 1
					if entry['delay_m'] > 0:
							station.delay += entry['delay_m']
					station.certainty = True if entry['certainty'] else False
					station.put()
		self.response.write('Done!')

mean = webapp2.WSGIApplication([
    ('/mean', Mean),
], debug=True)

