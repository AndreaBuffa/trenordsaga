from google.appengine.ext import ndb


class DelayCounter(ndb.Model):
  delayInMinutes = ndb.IntegerProperty()
  counter = ndb.IntegerProperty()

class TrainStop(ndb.Model):
	"""Models a generic station"""
	trainid = ndb.StringProperty(indexed = True)
	name = ndb.StringProperty(indexed = True)
	numofsurveys = ndb.IntegerProperty(indexed = False)
	delaysList = ndb.StructuredProperty(DelayCounter, repeated = True, indexed = False)
	startdate = ndb.DateProperty(indexed = False)
	certainty = ndb.BooleanProperty(indexed = False)

	def updateDelayCounter(self, _delayInMinutes):
		entries = filter(lambda delayCounter: delayCounter.delayInMinutes == _delayInMinutes,
			self.delaysList)
		if len(entries) == 1:
			entries[0].counter += 1
		elif len(entries) == 0:
			newEntry = DelayCounter()
			newEntry.delayInMinutes = _delayInMinutes
			newEntry.counter = 1
			self.delaysList.append(newEntry)
		elif len(entries) > 1:
			#log something wrong
			pass
		self.delaysList = sorted(self.delaysList,
			key=lambda delayCounter: delayCounter.delayInMinutes)
