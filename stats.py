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
					['Albairate Vermezzo', new Date(2014,12,15,0,5,0)],
					['GAGGIANO', new Date(2014,12,15,0,-2,0)],
					]);
			
				var options = {
					title: 'The decline of ',
					vAxis: {title: 'Accumulated Delay', maxValue: new Date(2014,12,15,1,0,0)},
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
