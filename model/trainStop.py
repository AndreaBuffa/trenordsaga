from google.appengine.ext import ndb

class TrainStop(ndb.Model):
	"""Models a generic station"""
	trainid = ndb.StringProperty(indexed=True)
	name = ndb.StringProperty(indexed=True)
	numofsurveys = ndb.IntegerProperty(indexed=False)
	delay = ndb.IntegerProperty(indexed=False)
	startdate = ndb.DateProperty(indexed=False)
	certainty = ndb.BooleanProperty(indexed=False)
