import webapp2
from model.dataProviderFactory import *
import model.s9
from model.trainStop import *
import common


class CroneTabPage(webapp2.RequestHandler):
	def get(self, trainId):
		myFactory = ChroneTab()
		myData = myFactory.createDataProvider()
		buffer = myData.RetrieveSourcePage()
		if buffer:
			timeSchedule = S9()
			timeSchedule.timings = buffer
			timeSchedule.trainId = trainId
			timeSchedule.put()
			stops = {}
			query = TrainStop.query(TrainStop.trainid == '24114')
			results = query.fetch()
			for record in results:
				stops[record.name] = record
			common.createTrainStop([timeSchedule], stops)
			for key, stop in stops.iteritems():
				stop.put()
		self.response.headers['Content-Type'] = 'text/plain'
		self.response.write('....Done!')

app = webapp2.WSGIApplication([
    ('/retrieve/(\d+)', CroneTabPage),
], debug=True)
