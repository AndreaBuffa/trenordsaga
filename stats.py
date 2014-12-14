import webapp2
import dataProvider
from dataProviderFactory import DataProviderFactory,FrontEnd
from scheduleParser import ScheduleParser

PAGE_TEMPLATE = """\
<html>
	<head>
		<script type="text/Javascript" src="https://www.google.com/jsapi"></script>
		<script type="text/Javascript">
			google.load("visualization", "1", {packages:["corechart"]});
			google.setOnLoadCallback(drawChart);
			function drawChart() {
				var data = google.visualization.arrayToDataTable([
					['Stazione',  'Delay'],
					['Albairate Vermezzo', 8.4],
					['GAGGIANO',     6.9],
					['TREZZANO S.N.',        6.5],
					['CESANO BOSCONE',      4.4],
					['CORSICO',      4.4],
					['MILANO S. CRISTOFORO',      4.4],
					['MILANO ROMOLO',      4.4],
					['MILANO PORTA ROMANA',      4.4],
					['MILANO LAMBRATE',      4.4],
					['MILANO GRECO PIRELLI',      4.4],
					['SESTO S. GIOVANNI',      4.4],
					['MONZA',      4.4],
					['LISSONE-MUGGIO`',      4.4],
					['DESIO',      4.4],
					['SEREGNO',      4.4],
					['BARRUCCANA',      4.4],
					['CESANO MADERNO',      4.4],
					['GROANE',      4.4],
					['CERLANO LAGHETTO',      4.4],
					['SARONNO SUD',      4.4],
					['SARONNO',      4.4]
					]);
			
				var options = {
					title: 'The decline of ',
					vAxis: {title: 'Accumulated Delay'},
					isStacked: true
				};
			
				var chart = new google.visualization.SteppedAreaChart(document.getElementById('chart_div'));
			
				chart.draw(data, options);
			}
		</script>
	</head>
	<body>
		<div id="chart_div" style="width: 900px; height: 500px;"></div>
	</body>
</html>
"""

class MainPage(webapp2.RequestHandler):
    def get(self):
		self.response.headers['Content-Type'] = 'text/html;'
		self.response.write(PAGE_TEMPLATE)
		myFactory = FrontEnd()
		myData = myFactory.createDataProvider()
		buffer = myData.RetrieveSourcePage()
		if buffer != None:
			myParser = ScheduleParser(buffer)
			self.response.write(myParser.GetTimings())
		#self.response.write(buffer)

app = webapp2.WSGIApplication([
    ('/', MainPage),
], debug=True)
