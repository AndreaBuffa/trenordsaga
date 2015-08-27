from google.appengine.ext import ndb

class Service(ndb.Model):
	"""Models a third-part service API"""
	description = ndb.StringProperty(indexed=False)
	name = ndb.StringProperty(indexed=True)
	URL = ndb.StringProperty(indexed=True)
