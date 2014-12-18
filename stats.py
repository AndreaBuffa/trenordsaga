import webapp2
import dataProvider
from dataProviderFactory import DataProviderFactory,FrontEnd
from scheduleParser import ScheduleParser
from formatter import Formatter

PAGE_TEMPLATE_1 = """\
<html>
	<head>
		<script type="text/Javascript" src="https://www.google.com/jsapi"></script>
		<script type="text/Javascript">
			google.load("visualization", "1", {packages:["corechart"]});
			google.setOnLoadCallback(drawChart);
			function drawChart() {
				var data = google.visualization.arrayToDataTable([
					['Stazione',  'Previsto', 'Ritardo'],
"""

PAGE_TEMPLATE_2 = """\
					]);

				var options = {
					title: 'Tabella dei tempi S9 di oggi',
					vAxis: {title: ''}
				};
			
				var chart = new google.visualization.SteppedAreaChart(document.getElementById('chart_div'));
			
				chart.draw(data, options);
			}
		</script>
	</head>
	<body>
		<div id="chart_div" style="height: 500px;"></div>
	</body>
</html>
"""

class MainPage(webapp2.RequestHandler):
    def get(self):
		self.response.headers['Content-Type'] = 'text/html;'
		self.response.write(PAGE_TEMPLATE_1)
		myFactory = FrontEnd()
		myData = myFactory.createDataProvider()
		buffer = myData.RetrieveSourcePage()
		if buffer != None:
			myParser = ScheduleParser(buffer)
			myFormatter = Formatter(myParser.GetTimings())
			chartData = myFormatter.ToGChartsDataTable()
			if chartData:
				self.response.write(chartData)
		self.response.write(PAGE_TEMPLATE_2)
		#self.response.write(buffer)

app = webapp2.WSGIApplication([
    ('/', MainPage),
], debug=True)
