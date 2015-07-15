MYAPP.View.TrainSelector.prototype.onClick = function(trainDescriptor) {
	if (this.notifyControl) {
		this.notifyControl.value = trainDescriptor.trainId;
	}
}

var myModel = new MYAPP.Model();

var trainSelector = new MYAPP.View.TrainSelector(myModel, document.querySelector('input[name="trainid"]'));
myModel.addObserver(trainSelector);

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
			maxDate: new Date(today.getFullYear(), today.getMonth(), today.getDate() - 1),
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
	google.load("visualization", "1", {packages:["corechart"],
		callback : function(){ drawCharts(); }});
}
