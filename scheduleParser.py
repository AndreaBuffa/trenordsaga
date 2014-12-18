import re
from datetime import datetime

class ScheduleParser:
	theString = ""
	stations = []

	def __init__(self, stringToParse=""):
		self.theString = stringToParse

	def AddStation(self, name, noticed, expectedTime, currentTime, delay):
		station = {}
		#print "%s, %d, %d, %d, %d" % (name, noticed, expectedTime, currentTime, delay)
		station['name'] = name if noticed else ("(%s)" % name)
		station['noticed'] = noticed
		station['sched_h'] = int(expectedTime / 60)
		station['sched_m'] = expectedTime % 60
		if noticed:
			station['real_h'] = int(currentTime / 60)
			station['real_m'] = currentTime % 60
		else:
			station['real_h'] = int(expectedTime / 60) + (delay / 60)
			station['real_m'] = expectedTime % 60 + (delay % 60)
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

	def Compress(self):
		return ""
