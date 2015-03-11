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
			if cmd == 'reset':
				trainstops = TrainStop.query(TrainStop.trainid == '24114')
				ndb.delete_multi([key for key in trainstops.iter(keys_only = True)])
			#create new ones
			timings = S9.query(ndb.AND(S9.date >= startDate,
									S9.date <= endDate)).fetch()
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
			self.response.write(datetime.datetime.now())

mean = webapp2.WSGIApplication([
	(r'/mean/(\d{4}-\d{1,2}-\d{1,2})/(\d{4}-\d{1,2}-\d{1,2})/(reset)*', Mean)
], debug=True)
