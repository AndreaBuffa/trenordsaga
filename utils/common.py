import datetime
from model.trainStop import *
from view.scheduleParser import *

def createTrainStop(timings, stops):
	for record in timings:
		myParser = ScheduleParser(record.timings)
		timeSchedule = myParser.GetTimings()
		for entry in timeSchedule:
			if not stops.has_key(entry['name']):
				station = TrainStop()
				station.name = entry['name']
				station.trainid = '24114'
				station.startdate = datetime.strptime('2014-12-18', "%Y-%m-%d")
				station.numofsurveys = 0
				station.totDelay = 0
				station.delaysList = []
				stops[entry['name']] = station
			delay = entry['delay_m'] if entry['delay_m'] > 0 else 0
			stops[entry['name']].numofsurveys += 1
			stops[entry['name']].totDelay += delay
			stops[entry['name']].updateDelayCounter(delay)
			stops[entry['name']].certainty = True if entry['certainty'] else False