var model = MYAPP.Model();

var searchTrain = MYAPP.View.SearchTrain({'model': model, 'anchor': '#search'});
model.addObserver(COMM.event.modelReady, searchTrain);