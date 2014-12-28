import time
from datetime import date
class Formatter:
	timeSchedule = []

	def __init__(self, scheduleList):
		self.timeSchedule = scheduleList

	def ToGChartsDataTable(self):
		buffer = ""
		for entry in self.timeSchedule:
			print entry
			buffer = "%s%s ['%s', new Date(%s,%d,%d,0), new Date(%s,%d,%d,0)]" % \
				(buffer,
				',' if len(buffer) else '',
				entry['name'],
				date.today().strftime("%y,%m,%d"),
				entry['sched_h'],
				entry['sched_m'],
				date.today().strftime("%y,%m,%d"),
				entry['real_h'],
				entry['real_m'])
		return buffer
