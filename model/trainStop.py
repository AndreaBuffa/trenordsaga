from google.appengine.ext import ndb

class DelayCounter(ndb.Model):
  delayInMinutes = ndb.IntegerProperty()
  counter = ndb.IntegerProperty()

''' routine for incrementing the counter of a particular delay-in-minutes'''
def updateDelayCounter(delayList, _delayInMinutes):
	entries = filter(lambda delayCounter: delayCounter.delayInMinutes == _delayInMinutes,
		delayList)
	if len(entries) == 1:
		entries[0].counter += 1
	elif len(entries) == 0:
		newEntry = DelayCounter()
		newEntry.delayInMinutes = _delayInMinutes
		newEntry.counter = 1
		delayList.append(newEntry)
	elif len(entries) > 1:
		logging.debug('Unexpected multiple entries for delay %d', _delayInMinutes)

class TrainStop(ndb.Model):
	"""Models a generic station"""
	trainid = ndb.StringProperty(indexed = True)
	name = ndb.StringProperty(indexed = True)
	workDaySurveys = ndb.IntegerProperty(indexed = False)
	dayOffSurveys = ndb.IntegerProperty(indexed = False)
	workDayDelays = ndb.StructuredProperty(DelayCounter, repeated = True, indexed = False)
	dayOffDelays = ndb.StructuredProperty(DelayCounter, repeated = True, indexed = False)
	startdate = ndb.DateProperty(indexed = False)
	workDayTot = ndb.IntegerProperty(indexed = True)
	dayOffTot = ndb.IntegerProperty(indexed = True)
	certainty = ndb.BooleanProperty(indexed = False)

	def put(self):
		self.workDayDelays = sorted(self.workDayDelays,
			key=lambda delayCounter: delayCounter.delayInMinutes)
		self.dayOffDelays = sorted(self.dayOffDelays,
			key=lambda delayCounter: delayCounter.delayInMinutes)
		ndb.Model.put(self)

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
			logging.debug('Unexpected multiple entries for delay %d', _delayInMinutes)
