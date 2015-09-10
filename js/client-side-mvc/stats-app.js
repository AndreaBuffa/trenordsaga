
var myModel = MYAPP.Model({});

var trainStats = MYAPP.View.TrainStats({'model': myModel});
myModel.addObserver(COMM.event.modelReady, trainStats);


var trainSelector = MYAPP.View.TrainSelector({'model': myModel});
trainSelector.addObserver(COMM.event.trainChanged, trainStats);
myModel.addObserver(COMM.event.modelReady, trainSelector);

var searchTrain = MYAPP.View.SearchTrain({'model': myModel,
                                          'container': null});
myModel.addObserver(COMM.event.modelReady, searchTrain);

$(document).ready(function() {
	trainSelector.draw();
});
