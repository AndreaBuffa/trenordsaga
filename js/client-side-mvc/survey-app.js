MYAPP.View.TrainSelector.prototype.onClick = function(trainDescriptor) {
	if (this.notifyControl) {
		this.notifyControl.value = trainDescriptor.trainId;
	}
}

var myModel = new MYAPP.Model();

var trainSelector = new MYAPP.View.TrainSelector(myModel, document.querySelector('input[name="trainid"]'));
myModel.addObserver(trainSelector);

$(document).ready(function() {
	$(function() {
		$("[id^=datepicker]" ).datepicker({
			dateFormat: "yy-mm-dd",
			minDate: new Date(2014, 12 - 1, 18),
			maxDate: new Date(),
			defaultDate: "{{ date|safe|escape }}",
			onSelect: function(selectedDate) {
				document.form.postBttnBottom.disabled = false;
				document.form.postBttnTop.disabled = false;
				document.form.datetime.value = selectedDate;
		}});
	});

	google.load("visualization", "1", {packages:["corechart"],
		callback : function(){ drawCharts(); }});

	trainSelector.draw();
});
