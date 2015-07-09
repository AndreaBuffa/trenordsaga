MYAPP.View.TrainSelector.prototype.onClick = function(trainDescriptor) {
	//@todo
	if (this.notifyControl) {
		this.notifyControl.update(trainDescriptor);
	}
}

var myModel = new MYAPP.Model();

var trainSelector = new MYAPP.View.TrainSelector(myModel, null);
myModel.addObserver(trainSelector);

$(document).ready(function() {
	trainSelector.draw();
});
