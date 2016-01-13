import time
from datetime import date
from nls.nls import *

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
		delayBuf = b""
		for entry in timeSchedule:
			if entry['certainty']:
				certainty = 1
				certaintyBuf = "true"
			elif certainty:
				certaintyBuf = "true"
				certainty = 0
			else:
				certaintyBuf = "false"

			delayBuf = b"%02d:%02d" % (entry['real_h'], entry['real_m'])
			if entry['delay_m'] < 0:
				delayBuf = b"%s, %s" % (delayBuf, langSupport.get("early"))
			elif entry['delay_m'] == 0:
				delayBuf = b"%s, %s" % (delayBuf, langSupport.get("on_time"))
			elif entry['delay_m'] == 1:
				delayBuf = b"%s (1 %s)" % (delayBuf, langSupport.get("minute"))
			else:
				delayBuf = b"%s (%d %s)" %  (delayBuf, entry['delay_m'],
					langSupport.get("minutes"))

			buffer = b'%s%s{"c": [{"v": "%s", "f": null}, ' \
				  '{"v": [%d,%d,0,0], "f":null}, ' \
				  '{"v": [%d,%d,0,0], "f": "%s"}, ' \
				  '{"v": %s, "f": "test"}]}' % \
				  (buffer, ',' if len(buffer) else '',
				   entry['name'], entry['sched_h'],
				   entry['sched_m'], entry['real_h'],
				   entry['real_m'], delayBuf, certaintyBuf)

		buffer = b"""{"cols": [{"label": "stop", "pattern": "", "type": "string"},
				     {"label": "%s", "pattern": "", "type": "timeofday"},
				     {"label": "%s", "pattern": "", "type": "timeofday"},
				     {"type": "boolean", "p": {"role": "certainty"}}
				    ],
			      "rows": [%s ]
			     }""" % (langSupport.get("schedule"),
				     langSupport.get("real"),
				     buffer)

		return buffer

	def ToColumnChartJSon(self, timeSchedule, delayDict, currDate):
		myBuffer = b"";
		for entry in timeSchedule:
			delay = 0
			median = delayDict[entry['name']]
			if entry['delay_m'] >= 0:
				delay = entry['delay_m']

			myBuffer = b"""%s%s{"c": [{"v": \"%s\", "f": null},
									  {"v": %d, "f":"%s"},
									  {"v": %d, "f":"%s"}]}""" % \
				(myBuffer,
				',' if len(myBuffer) else '',
				entry['name'],
				delay,
				"1 %s" % langSupport.get("minute") if delay == 1 else "%d %s" % (delay,
					langSupport.get("minutes")),
				 median,
				 "1 %s" % langSupport.get("minute") if median == 1 else "%d %s" % (median, langSupport.get("minutes")))

		niceDate = currDate.strftime(langSupport.get('date_format'))
		currDalayLabel = langSupport.get("delay") + " " + \
						langSupport.get("left_day") + " " + niceDate
		myBuffer = b"""{
				"cols": [
						{"label": "", "pattern": "", "type": "string"},
						{"label": "%s", "pattern": "", "type": "number"},
						{"label": "%s", "pattern": "", "type": "number"}],
				"rows": [%s ]}""" % (currDalayLabel,
								   langSupport.get("median_delay"),
								   myBuffer)

		return myBuffer

	def ToPieChartJSon(self, timeSchedule):
		myBuffer = b"";
		myTable = {}
		for stop in timeSchedule:
			delay = stop['delay_m']
			if delay < 0:
				delay = 0
			if myTable.has_key(delay):
				myTable[delay] += 1
			else:
				myTable[delay] = 1

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
