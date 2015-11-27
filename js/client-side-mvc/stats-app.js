
var myModel = MYAPP.Model({});

var trainSelector = MYAPP.View.TrainSelector({'model': myModel, 'anchor': '#search'});
myModel.addObserver(COMM.event.modelReady, trainSelector);

var trainStats = MYAPP.View.TrainStats({'model': myModel});
myModel.addObserver(COMM.event.modelReady, trainStats);
trainSelector.addObserver(COMM.event.trainChanged, trainStats);

var searchTrain = MYAPP.View.SearchTrain({'model': myModel, 'anchor': '#search'});
myModel.addObserver(COMM.event.modelReady, searchTrain);

var picker = MYAPP.View.TabView({'model': myModel, 'divId': '#menuPicker'});
console.log('Adding the picker');
picker.fillTabHeader(0, '1');
picker.fillTabContent(0, trainSelector);
picker.fillTabHeader(1, '2');
picker.fillTabHeader(2, '3');
myModel.addObserver(COMM.event.modelReady, picker);

$(document).ready(function() {
	trainSelector.draw();
});
