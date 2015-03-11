import webapp2
from model.dataProviderFactory import *
import model.s9
from model.railwayStation import *
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
				query = RailwayStation.query(ndb.AND(RailwayStation.name == entry['name'],
												RailwayStation.trainid == '24114'))
				station = query.get()
				if not station:
						station = RailwayStation()
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
		query = S9.query()
		timings = query.get()
		print timings
		for record in timings:
				myParser = ScheduleParser(record.timings)
				timeSchedule = myParser.GetTimings()
				for entry in timeSchedule:
						query = RailwayStation.query(ndb.AND(RailwayStation.name == entry['name'],
														RailwayStation.trainid == '24114'))
						station = query.get()
						if not station:
								station = RailwayStation()
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

