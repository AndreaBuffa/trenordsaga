import re
from datetime import datetime

class ScheduleParser:
	theString = ""
	stations = []

	def __init__(self, stringToParse=""):
		self.theString = stringToParse

	def AddStation(self, name, certainty, expectedTime, currentTime, delay):
		station = {}
		#print "%s, %d, %d, %d, %d" % (name, certainty, expectedTime, currentTime, delay)
		station['name'] = name.title()
		station['certainty'] = certainty
		station['sched_h'] = expectedTime / 60
		station['sched_m'] = expectedTime % 60
		if certainty:
			station['real_h'] = currentTime / 60
			station['real_m'] = currentTime % 60
		else:
			estimation = expectedTime + delay
			station['real_h'] = estimation / 60
			station['real_m'] = estimation % 60
		station['delay_m'] = delay
		self.stations.append(station.copy())
		#print station

	def GetTimings(self):
		self.stations = []
		lookForTime = 0
		expectedTime = 0
		currentTime = 0
		delay = 0
		stationName = ""
		for token in self.theString.split('<'):
			#print "(%s)" % (token)
			pattern = re.compile('^h2>(.+)')
			stationMatch = pattern.search(token)
			if stationMatch != None:
				if lookForTime:
					self.AddStation(stationName, 0, expectedTime, 0, delay)
					expectedTime = 0
				stationName = stationMatch.group(1)
				lookForTime = 1
			if lookForTime:
				pattern = re.compile('(\d{1,2})\:(\d{1,2})')
				time = pattern.search(token)
				if time:
					if expectedTime == 0:
						expectedTime = int(time.group(1)) * 60 + int(time.group(2))
					else:
						currentTime = int(time.group(1)) * 60 + int(time.group(2))
						delay = currentTime - expectedTime
						#buffer = "%s|%s=%s%02d:%02d" % (buffer, stationName, "-" if currentTime < expectedTime else "" , abs(delay) / 60, abs(delay) % 60)
						self.AddStation(stationName, 1, expectedTime, currentTime, delay)
						expectedTime = 0
						lookForTime = 0

		return self.stations

def extract_departures(trainListString):
	departures = []
	for token in trainListString.split('<'):
		pattern = re.compile('(\d{1,2})\:(\d{1,2})')
		if lookForDepartureTime:
			departureTime = pattern.search(token)
		elif lookForArrivalTime:
			arrivalTime = pattern.search(token)

def extract_links(trainListString):
	hrefList = []
	for token in trainListString.split('<'):
		match = re.compile('^a href="').search(token)
		if not match:
			continue
		# check it's the link I need
		match1 = re.compile('sessionId').search(token)
		if not match1:
			continue
		queryString = re.compile('\?(.+)').search(token)
		href = token[queryString.start():]

		match2 = re.compile('(.+)"').search(href)
		if not match2:
			continue
		href = match2.group(1)

		hrefList.append(href)
	return hrefList

def extract_train_details(trainList):
	return []
