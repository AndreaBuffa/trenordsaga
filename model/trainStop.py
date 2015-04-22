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

	def getMediana(self, workDay=True, dayOff=True):
		if len(self.workDayDelays) == 0 and len(self.workDayDelays) == 0:
			return 0.0

		if (dayOff and workDay):
			if len(self.workDayDelays) == 0 and len(self.dayOffDelays) > 0:
				samples = self.dayOffDelays
			elif len(self.workDayDelays) > 0 and len(self.dayOffDelays) == 0:
				samples = self.workDayDelays
			else:
				dayOffIndex = 0
				workDayIndex = 0
				while True:
					if self.workDayDelays[workDayIndex].delayInMinutes < self.dayOffDelays[dayOffIndex].delayInMinutes:
						sample.append(self.workDayDelays[workDayIndex])
						if workingDayIndex < len(self.workDayDelays):
							workingDayIndex += 1
					elif self.workDayDelays[workDayIndex].delayInMinutes > self.dayOffDelays[dayOffIndex].delayInMinutes:
						sample.append(self.dayOffDelays[dayOffIndex])
						if dayOffIndex < len(self.dayOffDelays):
							dayOffIndex += 1
					else:
						newSample = DelayCounter()
						newSample.delayInMinutes = self.dayOffDelays[workDayIndex].delayInMinutes
						newSample.counter = self.dayOffDelays[dayOffIndex].counter + self.workDayDelays[workDayIndex].counter
					if dayOffIndex >= len(self.workDayDelays) and workDayIndex >= len(self.workDayDelays):
						break

			sampleIndex = self.workDaySurveys + self.dayOffSurveys
			isEven = (sampleIndex % 2 == 0)

		else:
			if workDay:
				samples = self.workDayDelays
				sampleIndex = self.workDaySurveys
				isEven = (self.workDaySurveys % 2 == 0)
			if dayOff:
				samples = self.dayOffDelays
				sampleIndex = self.dayOffSurveys
				isEven = (self.dayOffSurveys % 2 == 0)
		if isEven:
			sampleIndex = sampleIndex / 2 - 1
		else:
			sampleIndex = (sampleIndex + 1) / 2 - 1

		counter = 0
		index = 0
		for sample in samples:
			if counter >= sampleIndex:
				if isEven:
					if sample.counter > 1:
						return float(sample.delayInMinutes)
					else:
						return float((sample.delayInMinutes + samples[index+1].delayInMinutes) / 2)
				else:
					return float(sample.delayInMinutes)
			index += 1
			counter += sample.counter
		return 0.0
