from google.appengine.ext import ndb
import logging

''' for each delay delayInMinutes, counter is the number of time this delay happend'''
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
	"""the number of surveys taken during a weekday """
	workDaySurveys = ndb.IntegerProperty(indexed = False)
	"""the number of surveys taken during a weekend or a day off """
	dayOffSurveys = ndb.IntegerProperty(indexed = False)
	"""List of DelayCounter, (1 min, 10 times), (2 mins, 14 times).. ordered by delay"""
	workDayDelays = ndb.StructuredProperty(DelayCounter, repeated = True, indexed = False)
	"""List of DelayCounter, (1 min, 10 times), (2 mins, 14 times).. ordered by delay"""
	dayOffDelays = ndb.StructuredProperty(DelayCounter, repeated = True, indexed = False)
	"""the date of the first survey for this station name and this train id"""
	startdate = ndb.DateProperty(indexed = False)
	"""The sum of all the delays during the weekday for this station and this train id"""
	workDayTot = ndb.IntegerProperty(indexed = True)
	"""The sum of all the delays during holidays for this station and this train id"""
	dayOffTot = ndb.IntegerProperty(indexed = True)
	"""True/false If the datasource provides a certain value for this station or not"""
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

	def getMedian(self, workDay=True, dayOff=True):
		numWorkDays = len(self.workDayDelays)
		numDaysOff = len(self.dayOffDelays)
		if (numWorkDays == 0) and (numDaysOff == 0):
			return 0.0
		# choose the samples, dayOff/ working day/ both
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
					#logging.debug('Indices %d %d %d %d', dayOffIndex, numDaysOff, workDayIndex, numWorkDays)
					# one of the two lists's been traversed
					if workDayTail and not dayOffTail:
						samples.extend(self.dayOffDelays[dayOffIndex:])
						dayOffTail = True
						break
					if dayOffTail and not workDayTail:
						samples.extend(self.workDayDelays[workDayIndex:])
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
						# merge two elems with the same delayInMinutes. It means
						# the same delayInMinutes, and the counters summed.
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
		# compute median sample index
		if isEven:
			sampleIndex = numSamples / 2 - 1
		else:
			sampleIndex = (numSamples + 1) / 2 - 1
		# traversing samples list in order to get the median index
		counter = index = 0
		for sample in samples:
			counter += sample.counter
			logging.debug('%s: sampleIndex %d counter %d index %d', self.name, sampleIndex, counter, index)
			if counter >= sampleIndex:
				if isEven:
					if counter - sampleIndex> 1:
						return float(sample.delayInMinutes)
					else:
						return float(sample.delayInMinutes + samples[index+1].delayInMinutes) / 2
				else:
					return float(sample.delayInMinutes)
			index += 1
		return 0.0
