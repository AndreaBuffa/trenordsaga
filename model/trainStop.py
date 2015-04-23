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
		numWorkDays = len(self.workDayDelays)
		numDaysOff = len(self.dayOffDelays)
		if (numWorkDays == 0) and (numDaysOff == 0):
			return 0.0

		samples = []
		if (dayOff and workDay):
			# merge two sorted lists, workDayDelays and dayOffDelays
			if numWorkDays == 0 and numDaysOff > 0:
				samples = self.dayOffDelays
			elif numWorkDays > 0 and numDaysOff == 0:
				samples = self.workDayDelays
			else:
				dayOffIndex = workDayIndex = 0
				workDayTail = dayOffTail = False
				while not workDayTail or not dayOffTail:
					logging.debug('Indices %d %d %d %d', dayOffIndex, numDaysOff, workDayIndex, numWorkDays)
					# one of the two lists's been traversed
					if workDayTail and not dayOffTail:
						samples.extend(dayOffDelays[dayOffIndex:])
						dayOffTail = True
						break
					if dayOffTail and not workDayTail:
						samples.extend(workDayDelays[workDayIndex:])
						workDayTail = True
						break
					# traversing both lists.
					workDayCounter = self.workDayDelays[workDayIndex]
					dayOffCounter = self.dayOffDelays[dayOffIndex]
					if workDayCounter.delayInMinutes < dayOffCounter.delayInMinutes:
						samples.append(workDayCounter)
						if workDayIndex < numWorkDays - 1:
							workDayIndex += 1
						else:
							workDayTail = True
					elif workDayCounter.delayInMinutes > dayOffCounter.delayInMinutes:
						samples.append(dayOffCounter)
						if dayOffIndex < numDaysOff - 1:
							dayOffIndex += 1
						else:
							dayOffTail = True
					else:
						newSample = DelayCounter()
						newSample.delayInMinutes = dayOffCounter.delayInMinutes
						newSample.counter = dayOffCounter.counter + workDayCounter.counter
						samples.append(newSample)

						if workDayIndex < numWorkDays - 1:
							workDayIndex += 1
						else:
							workDayTail = True
						if dayOffIndex < numDaysOff - 1:
							dayOffIndex += 1
						else:
							dayOffTail = True
			numSamples = self.workDaySurveys + self.dayOffSurveys
			isEven = (numSamples % 2 == 0)

		else:
			if workDay:
				samples = self.workDayDelays
				numSamples = self.workDaySurveys
				isEven = (self.workDaySurveys % 2 == 0)
			if dayOff:
				samples = self.dayOffDelays
				numSamples = self.dayOffSurveys
				isEven = (self.dayOffSurveys % 2 == 0)
		if isEven:
			sampleIndex = numSamples / 2 - 1
		else:
			sampleIndex = (numSamples + 1) / 2 - 1

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
