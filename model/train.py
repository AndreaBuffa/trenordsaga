from google.appengine.ext import ndb

class Train(ndb.Model):
	"""Models an individual Schedule entry for a particular train"""
	date = ndb.DateProperty(auto_now_add=True)
	timings = ndb.StringProperty(indexed=False)
	trainId = ndb.StringProperty(indexed=True)