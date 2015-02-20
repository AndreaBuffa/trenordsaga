'''Simple Native Language Support
	en-US/it-IT
'''
import re
class NLS(object):
	entries = {}
	currLang = ""
	default = "en-US"

	def __new__(cls):
		if not hasattr(cls, 'instance'):
			cls.instance = super(NLS, cls).__new__(cls)
		return cls.instance

	def __init__(self, lang="en-US"):
		self.default = lang
		self.currLang = self.default
		self.entries['title'] = {
					'en-US': 'Trenord Saga'}
		self.entries['on_time_stops'] = {
					'en-US': 'On time stops:',
					'it-IT': 'Fermate in orario'}
		self.entries['survey'] = {
					'en-US': 'Survey on date',
					'it-IT': 'Rilevazione del'}
		self.entries['none'] = {
					'en-US': 'None',
					'it-IT': 'Nessuna'}
		self.entries['grouped_by_delay'] = {
					'en-US': 'Stops grouped by delay:',
					'it-IT': 'Fermate raggruppate per ritardo:'}
		self.entries['ordered_by_delay'] = {
					'en-US': 'Stops ordered by delay:',
					'it-IT': 'Le fermate in ordine di ritardo:'}
		self.entries['delay_in_minutes'] = {
					'en-US': 'Delay in minutes',
					'it-IT': 'Ritardo in minuti'}
		self.entries['schedule'] = {
					'en-US': 'Schedule',
					'it-IT': 'Previsto'}
		self.entries['real'] = {
					'en-US': 'Real',
					'it-IT': 'Effettivo'}
		self.entries['delay'] = {
					'en-US': 'Delay',
					'it-IT': 'Ritardo'}

	def setLang(self, acceptLang):
		match = re.compile('it-IT').search(acceptLang)
		if match:
			self.currLang = "it-IT"
		else:
			self.currLang = "en-US"

	def get(self, entry):
		if not entry:
			return ""
		if self.entries.has_key(entry):
			if self.entries[entry].has_key(self.currLang):
				return self.entries[entry][self.currLang]
			else:
				if self.currLang != self.default:
					return self.entries[entry][self.default]
		else:
			return entry

	def getEntries(self):
		ret = {}
		for key, value in self.entries.iteritems():
			ret[key] = self.get(key)
		return ret

langSupport = NLS()
