#!/usr/bin/env python
import re, urllib

url="http://mobile.my-link.it/mylink/mobile/scheda?dettaglio=visualizza&numeroTreno=24108&codLocOrig=S01059&tipoRicerca=numero&lang=IT"
print "Getting page"
#f = open('datasetS9.html','r')
#print f.read()
#for match in re.findall('<h2>.*\d{1,2}\:\d{1,2}', urllib.urlopen(url).read()):
#for match in re.findall('\d{1,2}\:\d{1,2}', f.read()):
#	print match
buffer = "Today:"
with open('datasetS9.html') as fh:
	entry = 0
	expected = 0
	real = 0
	for line in iter(fh.readline, ''):
		if entry == 0:
			entryMatch = re.search('Arrivo Programmato', line)
			if entryMatch != None:
				entry = 1
			else:
				entryMatch = re.search('Partenza programmata', line)
				if entryMatch != None:
					entry = 1
					#print "Nuova partenza"
		if entry == 1:
	 		time = re.search('\d{1,2}\:\d{1,2}', line)
			if time != None:
				if expected == 0:
					expected = 1
				if expected == 1:
					real = 1
					expected = 0
					entry = 0 
				#print time.group(0)
				buffer = buffer + " " + time.group(0)
print buffer
