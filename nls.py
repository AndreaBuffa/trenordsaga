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
		self.entries['name'] = {
					'en-US': 'Trenord Saga'}
		self.entries['home'] = {
					'en-US': 'Home'}
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
					'it-IT': 'Nessuna!'}
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
		self.entries['banner_title'] = {
					'en-US': 'This is a saga, but always the same tale',
					'it-IT': 'una saga, ma &egrave; sempre la stessa storia?'}
		self.entries['banner_title_sub'] = {
					'en-US': 'Performance Albairate-Saronno line',
					'it-IT': 'Le performance del treno Albairate-Saronno delle 8:08'}
		self.entries['learn_more'] = {
					'en-US': 'Learn more',
					'it-IT': 'Per saperne di pi&ugrave;'}
		self.entries['daily'] = {
					'en-US': 'Daily',
					'it-IT': 'Giorno per giorno'}
		self.entries['statistics'] = {
					'en-US': 'Statistics',
					'it-IT': 'Statistiche'}
		self.entries['about'] = {
					'en-US': 'About',
					'it-IT': 'Progetto'}
		self.entries['aboutme'] = {
					'en-US': 'About Me',
					'it-IT': 'Su di me:'}
		self.entries['nosurvey'] = {
					'en-US': 'Today survey available after 10:30 pm CET. Past surveys are coming soon.',
					'it-IT': 'Le rilevazioni di oggi sono disponibili dopo le 10:30. A breve la possibilit&agrave; di visualizzare le rilevazioni per data.'}


	def setLang(self, acceptLang):
		match = re.compile('it-IT').search(acceptLang)
		if match:
			self.currLang = "it-IT"
		else:
			self.currLang = "en-US"

	def get(self, entry):
		if not entry:
			return "ERROR-EMPTY-KEY"
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
