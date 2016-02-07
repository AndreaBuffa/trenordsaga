import time
from datetime import date
from model.trainStop import *
from parser import *

def createTrainStop(record, stops):
    if not record:
        return
    myParser = ScheduleParser(record.timings)
    parsedStopList = myParser.GetTimings()
    idx = 0
    for entry in parsedStopList:
        if not stops.has_key(entry['name']):
            station = TrainStop()
            station.name = entry['name']
            station.trainid = record.trainId
            station.startdate = record.date
            station.workDaySurveys = 0
            station.dayOffSurveys = 0
            station.workDayTot = 0
            station.dayOffTot = 0
            station.workDayDelays = []
            station.dayOffDelays = []
            stops[entry['name']] = station
        delay = entry['delay_m'] if entry['delay_m'] > 0 else 0
        if isWorkDay(record.date) == True:
            stops[entry['name']].workDaySurveys += 1
            stops[entry['name']].workDayTot += delay
            updateDelayCounter(stops[entry['name']].workDayDelays, delay)
        else:
            stops[entry['name']].dayOffSurveys += 1
            stops[entry['name']].dayOffTot += delay
            updateDelayCounter(stops[entry['name']].dayOffDelays, delay)
        stops[entry['name']].certainty = True if entry['certainty'] else False
        stops[entry['name']].index = idx
        idx += 1

def isWorkDay(theDate):
	if theDate.weekday() > 4:
		return False
	for t in (date(theDate.year,  1,  1), "Capodanno"), \
		(date(theDate.year,  1,  6), "Epifania"), \
		(date(theDate.year,  4,  6), "Lunedi dell'Angelo"), \
		(date(theDate.year,  4, 25), "Anniversario della Liberazione"), \
		(date(theDate.year,  5,  1), "Festa del Lavoro"), \
		(date(theDate.year,  6,  2), "Festa della Repubblica"), \
		(date(theDate.year,  8, 15), "Assunzione di Maria Vergine"), \
		(date(theDate.year, 11,  2), "Tutti i Santi"), \
		(date(theDate.year, 12,  8), "Immacolata Concezione"), \
		(date(theDate.year, 12, 25), "Natale"), \
		(date(theDate.year, 12, 26), "Santo Stefano"):
		if theDate == t[0]:
			return False
	return True

def buildDate(y, m, d, ret):
	if y and m and d:
		try:
			ret.append(datetime.strptime(y + "-" + m + "-" + d,
			                             "%Y-%m-%d").date())
		except ValueError:
			return False
	else:
		return False
	return True
