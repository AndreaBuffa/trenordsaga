
class Formatter:
	timeSchedule = []

	def __init__(self, scheduleList=[]):
		timeSchedule = scheduleList

	def ToGChartsDataTable(self):
		buffer = ""
		for entry in self.timeSchedule:
			buffer = "%s, ['%s', new Date(%s,%d,%d)]" % (buffer, entry[0], time.strptime(date.today(), "%Y,%m,%d", entry[1]))
		return buffer
