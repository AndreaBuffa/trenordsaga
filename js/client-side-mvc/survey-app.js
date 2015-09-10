var control = COMM.Observer({});
control.trigger = function(eventName, params) {
    document.form.trainid.value = params.trainId;
}

var myModel = MYAPP.Model();

var trainSelector = MYAPP.View.TrainSelector({'model': myModel});
myModel.addObserver(COMM.event.modelReady, trainSelector);
trainSelector.addObserver(COMM.event.trainChanged, control);

$(document).ready(function() {
	trainSelector.draw();
});

//$(window).load(function() {
//});

window.onload = function() {
	const today = new Date();
	$(function() {
		$("[id^=datepicker]" ).datepicker({
			dateFormat: "yy-mm-dd",
			minDate: "{{ minDate|safe|escape }}",
			maxDate: new Date(today.getFullYear(),
					  today.getMonth(),
					  today.getDate() - 1),
			defaultDate: "{{ currDate|safe|escape }}",
			 onSelect: function(selectedDate) {
				if (document.form.postBttnBottom) {
					document.form.postBttnBottom.disabled = false;
				}
				if (document.form.postBttnTop) {
					document.form.postBttnTop.disabled = false;
				}
				document.form.datetime.value = selectedDate;
		}});
	});
	if (typeof(google) !== "undefined") {
		google.load("visualization", "1",
			    { packages: ["corechart"],
			      callback: function() { drawCharts(); }});
	}
}
