from google.appengine.ext import ndb

class TrainDescr(ndb.Model):
	trainId = ndb.StringProperty(indexed=True)
	type = ndb.StringProperty(indexed=True)
	url = ndb.StringProperty(indexed=True)
	leaveStation = ndb.StringProperty(indexed=True)
	endStation = ndb.StringProperty(indexed=True)
	arriveTime = ndb.StringProperty(indexed=True)
	leaveTime = ndb.StringProperty(indexed=True)
	date = ndb.DateProperty(indexed=True)
	status = ndb.StringProperty(indexed=True)

	def getIsoFormatDate(self):
		if self.date:
			return self.date.isoformat()
