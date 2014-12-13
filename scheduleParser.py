import re
from datetime import datetime

class ScheduleParser:
	theString = ""
	SCHEDULED_DEP_TOK = "Partenza programmata"
	SCHEDULED_ARR_TOK = "Arrivo Programmato"

	def __init__(self, stringToParse=""):
		self.theString = stringToParse


	def GetTimings(self):
		buffer = ""
		lookForTime = False
		lookForDeparture = True
		expectedTime = 0
		currentTime = 0
		delay = 0
		tokenList = self.theString.split('<')
		for token in tokenList:
			if lookForDeparture:
				idx = token.find(self.SCHEDULED_DEP_TOK)
				if idx != -1:
					lookForTime = True
					lookForDeparture = False
			else:
				idx = token.find(self.SCHEDULED_ARR_TOK)
				if idx != -1:
					if lookForTime:
						buffer = "%s (%s%02d:%02d)" % (buffer, "-" if delay < 0 else "" , abs(delay) / 60, abs(delay) % 60)
					expectedTime = 0
					lookForTime = True
			if lookForTime:
				pattern = re.compile('(\d{1,2})\:(\d{1,2})')
				time = pattern.search(token)
				if time:
					if expectedTime == 0:
						expectedTime = int(time.group(1)) * 60 + int(time.group(2))
					else:
						lookForTime = False
						currentTime = int(time.group(1)) * 60 + int(time.group(2))
						delay = currentTime - expectedTime
						buffer = "%s %s%02d:%02d" % (buffer, "-" if currentTime < expectedTime else "" , abs(delay) / 60, abs(delay) % 60)
						expectedTime = 0
		return buffer

	def Compress(self):
		return ""
