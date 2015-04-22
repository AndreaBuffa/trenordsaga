from google.appengine.ext import ndb
import logging

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
		if (len(self.workDayDelays) == 0) and (len(self.dayOffDelays) == 0):
			return 0.0

		samples = []
		if (dayOff and workDay):
			if len(self.workDayDelays) == 0 and len(self.dayOffDelays) > 0:
				samples = self.dayOffDelays
			elif len(self.workDayDelays) > 0 and len(self.dayOffDelays) == 0:
				samples = self.workDayDelays
			else:
				dayOffIndex = workDayIndex = 0
				workDayTail = dayOffTail = False
				while not workDayTail or not dayOffTail:
					logging.debug('Indices %d %d %d %d', dayOffIndex, len(self.dayOffDelays), workDayIndex, len(self.workDayDelays))
					if self.workDayDelays[workDayIndex].delayInMinutes < self.dayOffDelays[dayOffIndex].delayInMinutes:
						samples.append(self.workDayDelays[workDayIndex])
						if workDayIndex < len(self.workDayDelays) - 1:
							workDayIndex += 1
						else:
							workDayTail = True
					elif self.workDayDelays[workDayIndex].delayInMinutes > self.dayOffDelays[dayOffIndex].delayInMinutes:
						samples.append(self.dayOffDelays[dayOffIndex])
						if dayOffIndex < len(self.dayOffDelays) - 1:
							dayOffIndex += 1
						else:
							dayOffTail = True
					else:
						newSample = DelayCounter()
						newSample.delayInMinutes = self.dayOffDelays[dayOffIndex].delayInMinutes
						newSample.counter = self.dayOffDelays[dayOffIndex].counter + self.workDayDelays[workDayIndex].counter
						samples.append(newSample)

						if workDayIndex < len(self.workDayDelays) - 1:
							workDayIndex += 1
						else:
							workDayTail = True
						if dayOffIndex < len(self.dayOffDelays) - 1:
							dayOffIndex += 1
						else:
							dayOffTail = True
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

		counter = index = 0
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
