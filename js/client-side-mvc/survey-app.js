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
