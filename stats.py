import webapp2
import dataProvider
from dataProviderFactory import DataProviderFactory,FrontEnd
from scheduleParser import ScheduleParser
from formatter import Formatter

PAGE_TEMPLATE_1 = """\
<html>"""

JS_TPL_H = """\
	<head>
		<script type="text/Javascript" src="https://www.google.com/jsapi"></script>
		<script type="text/Javascript">
			google.load("visualization", "1", {packages:["corechart"]});
			google.setOnLoadCallback(drawChart);
			function drawChart() {
				var data = google.visualization.arrayToDataTable([
					['Stazione',  'Previsto', 'Ritardo'],
"""

JS_TPL_F = """\
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
"""

PAGE_TEMPLATE_2 = """\
	<body>
		<div id="chart_div" style="height: 500px;"></div>
	</body>
</html>"""

class MainPage(webapp2.RequestHandler):
    def get(self):
		self.response.headers['Content-Type'] = 'text/html;'
		self.response.write(PAGE_TEMPLATE_1)
		myFactory = FrontEnd()
		myData = myFactory.createDataProvider()
		buffer = myData.RetrieveSourcePage()
		if buffer:
			myParser = ScheduleParser(buffer)
			myFormatter = Formatter(myParser.GetTimings())
			chartData = myFormatter.ToGChartsDataTable()
			if chartData:
				self.response.write(JS_TPL_H)
				self.response.write(chartData)
				self.response.write(JS_TPL_F)
		self.response.write(PAGE_TEMPLATE_2)
#self.response.write(buffer)

app = webapp2.WSGIApplication([
    ('/', MainPage),
], debug=True)
