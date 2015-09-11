
var myModel = MYAPP.Model({});

var trainSelector = MYAPP.View.TrainSelector({'model': myModel, 'anchor': '#search'});
myModel.addObserver(COMM.event.modelReady, trainSelector);

var trainStats = MYAPP.View.TrainStats({'model': myModel});
myModel.addObserver(COMM.event.modelReady, trainStats);
trainSelector.addObserver(COMM.event.trainChanged, trainStats);

var searchTrain = MYAPP.View.SearchTrain({'model': myModel, 'anchor': '#search'});
myModel.addObserver(COMM.event.modelReady, searchTrain);

$(document).ready(function() {
	trainSelector.draw();
});
