MYAPP.View.TrainSelector.prototype.onClick = function(trainDescriptor) {
	if (this.notifyControl) {
		this.notifyControl.update(trainDescriptor);
	}
}

var myModel = new MYAPP.Model();

var trainStats = new MYAPP.View.TrainStats(myModel);
myModel.addObserver(trainStats);

var trainSelector = new MYAPP.View.TrainSelector(myModel, trainStats);
myModel.addObserver(trainSelector);

$(document).ready(function() {
	trainSelector.draw();
});
