import time
from datetime import date
class Formatter:

	def ToGChartsDataTable(self, timeSchedule):
		buffer = b""
		for entry in timeSchedule:
			buffer = b"%s%s [\"%s\", new Date(%s,%d,%d,0), true, new Date(%s,%d,%d,0), false]" % \
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

	def ToLineChartJSon(self, timeSchedule):
		buffer = b""
		certainty = 1
		certaintyBuf = b"true"
		delayBuf = b"";
		for entry in timeSchedule:
			if entry['certainty']:
				certainty = 1
				certaintyBuf = "true"
			else:
				if certainty:
					certaintyBuf = "true"
					certainty = 0
				else:
					certaintyBuf = "false"

			if entry['delay_m'] < 0:
				delayBuf = "in anticipo!"
			elif entry['delay_m'] == 0:
				delayBuf = "in orario!"
			elif entry['delay_m'] == 1:
				delayBuf = "1 minuto"
			else:
				delayBuf = "%d minuti" % entry['delay_m']

			buffer = b"%s%s{c: [{v: \"%s\", f: null}, {v: [%d,%d,0,0], f:null}, {v: [%d,%d,0,0], f: \"%s\"}, {v: %s, f: null}]}" % \
				(buffer,
				',' if len(buffer) else '',
				entry['name'],
				entry['sched_h'],
				entry['sched_m'],
				entry['real_h'],
				entry['real_m'],
				delayBuf,
				certaintyBuf)

		buffer = b"""{
				cols: [
						{id: "", label: "Stazione", pattern: "", type: "string"},
						{id: "", label: "Previsto", pattern: "", type: "timeofday"},
						{id: "", label: "Ritardo", pattern: "", type: "timeofday"},
						{id: "", type: "boolean", p: {"role": "certainty"}}],
				rows: [%s ]}""" % buffer
		return buffer

	def ToColumnChartJSon(self, timeSchedule):
		myBuffer = b"";
		for entry in timeSchedule:
			if entry['delay_m'] >= 10:
				hexColor = "#FF0000"
			elif entry['delay_m'] >= 5:
				hexColor = "#B20000"
			elif entry['delay_m'] >= 2:
				hexColor = "#FF8800"
			else:
				hexColor = "#FFFF00"

			myBuffer = b"%s%s{c: [{v: \"%s\", f: null}, {v: %d, f:\"%s\"}, {v: 'color: %s', f: null}]}" % \
				(myBuffer,
				',' if len(myBuffer) else '',
				entry['name'],
				entry['delay_m'],
				"1 minuto" if entry['delay_m'] == 1 else "%d minuti" % entry['delay_m'],
				hexColor)

		myBuffer = b"""{
				cols: [
						{label: "Stazione", pattern: "", type: "string"},
						{label: "Ritardo", pattern: "", type: "number"},
						{type: "string", p: {"role": "style"}}],
				rows: [%s ]}""" % myBuffer
		return myBuffer

	def ToPieChart(self, timeSchedule):
		myBuffer = b"";
		myTable = {}
		for stop in timeSchedule:
			if stop['delay_m'] < 0:
				stop['delay_m'] = 0
			if myTable.has_key(stop['delay_m']):
				myTable[stop['delay_m']] += 1
			else:
				myTable[stop['delay_m']] = 1

		for key, value in myTable.iteritems():
			myBuffer = b"%s%s{c: [{v: '%d', f: '%d %s in %s %s'}, {v: %d, f: null}]}" % \
				(myBuffer,
				',' if len(myBuffer) else '',
				key,
				value,
				"fermate" if value > 1 else "fermata",
				"ritarto" if key > 0 else "orario",
				"di %d min" % key if key > 0 else "",
				value)

		myBuffer = b"""{
				cols: [
						{label: "Num Stazioni", pattern: "", type: "string"},
						{label: "Ritardo in minuti", pattern: "", type: "number"}],
				rows: [%s ]}""" % myBuffer
		return myBuffer
