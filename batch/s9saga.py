#!/usr/bin/env python
import re, urllib
from datetime import datetime
from dateutil.parser import parse

url="http://mobile.my-link.it/mylink/mobile/scheda?dettaglio=visualizza&numeroTreno=24108&codLocOrig=S01059&tipoRicerca=numero&lang=IT"
print "Getting page"
#f = open('datasetS9.html','r')
#print f.read()
#for match in re.findall('<h2>.*\d{1,2}\:\d{1,2}', urllib.urlopen(url).read()):
#for match in re.findall('\d{1,2}\:\d{1,2}', f.read()):
#	print match
buffer = str(datetime.now().strftime('%Y-%m-%d %H:%M')) + ":"
with open('datasetS9.html') as fh:
	entry = 0
	expectedTime = ""
	delay = ""
	for line in iter(fh.readline, ''):
		entryMatch = re.search('Arrivo Programmato', line)
		if entryMatch != None:
			expectedTime = ""
			if entry == 1:
				buffer += "|" + delay
			entry = 1
		else:
			entryMatch = re.search('Partenza programmata', line)
			if entryMatch != None:
				expectedTime = ""
				if entry == None:
					buffer += "|" + delay
				entry = 1
		if entry == 1:
	 		time = re.search('\d{1,2}\:\d{1,2}', line)
			if time != None:
				if expectedTime == "":
					expectedTime = time.group(0)
				else:
					entry = 0
					delay = str((parse(time.group(0)) - parse(expectedTime)).total_seconds() / 60); 
					buffer += " " + delay
					expectedTime = ""
print buffer
