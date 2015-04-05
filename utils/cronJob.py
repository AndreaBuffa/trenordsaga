import webapp2
from model.dataProviderFactory import *
from model.train import *
from model.trainStop import *
import common


class CronPage(webapp2.RequestHandler):
	def get(self, trainId):
		myFactory = CronTab()
		myData = myFactory.createDataProvider(trainId)
		buffer = myData.RetrieveSourcePage()
		if buffer:
			timeSchedule = Train()
			timeSchedule.timings = buffer
			timeSchedule.trainId = trainId
			timeSchedule.put()
			stops = {}
			query = TrainStop.query(TrainStop.trainid == trainId)
			results = query.fetch()
			# build a dictionary
			for record in results:
				stops[record.name] = record
			common.createTrainStop([timeSchedule], stops)
			for key, stop in stops.iteritems():
				stop.put()
		self.response.headers['Content-Type'] = 'text/plain'
		self.response.write('....Done!')

app = webapp2.WSGIApplication([
    ('/retrieve/(\d+)', CronPage),
], debug=True)
