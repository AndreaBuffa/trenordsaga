from google.appengine.ext import ndb

class S9(ndb.Model):
	"""Models an individual Schedule entry."""
	date = ndb.DateProperty(auto_now_add=True)
	timings = ndb.StringProperty(indexed=False)
	trainId = ndb.StringProperty(indexed=True)