import time
from datetime import date
class Formatter:
	timeSchedule = []

	def __init__(self, scheduleList):
		self.timeSchedule = scheduleList

	def ToGChartsDataTable(self):
		buffer = ""
		for entry in self.timeSchedule:
			buffer = "%s%s [\"%s\", new Date(%s,%d,%d,0), true, new Date(%s,%d,%d,0), false]" % \
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

	def ToGChartJSon(self):
		buffer = b""
		certainty = 1
		certaintyBuf = b"true"
		delayBuf = b"";
		for entry in self.timeSchedule:
			# example
			# {c: [{v: "ALBAIRATE VERMEZZO", f: null}, {v: [8,8,0,0], f: null}, {v: [8,15,0,0], f: "5 min"}, {v: true, f: null}]},
			if entry['certainty']:
				certainty = 1
				certaintyBuf = "true"
			else:
				if certainty:
					certaintyBuf = "true"
					certainty = 0
				else:
					certaintyBuf = "false"

			if entry['delay_m'] == 0:
				delayBuf = "in orario!"
			elif entry['delay_m'] == 1:
				delayBuf = "1 minuto"
			else:
				delayBuf = "%d minuti" % entry['delay_m']

			buffer = "%s%s{c: [{v: \"%s\", f: null}, {v: [%d,%d,0,0], f:null}, {v: [%d,%d,0,0], f: \"%s\"}, {v: %s, f: null}]}" % \
				(buffer,
				',' if len(buffer) else '',
				entry['name'],
				entry['sched_h'],
				entry['sched_m'],
				entry['real_h'],
				entry['real_m'],
				delayBuf,
				certaintyBuf)

		ret = b"""{
				cols: [
						{id: "", label: "Stazione", pattern: "", type: "string"},
						{id: "", label: "Previsto", pattern: "", type: "timeofday"},
						{id: "", label: "Ritardo", pattern: "", type: "timeofday"},
						{id: "", type: "boolean", p: {"role": "certainty"}}],
				rows: [%s ]}""" % buffer
		return ret
