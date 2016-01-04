//$(window).load(function() {
//});

window.onload = function() {
	if (typeof(google) !== "undefined") {
		google.load("visualization", "1",
                {packages: ["corechart"],
                 callback: function() { drawCharts(); }});
	}
}
