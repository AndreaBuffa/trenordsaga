
var model = MYAPP.Model({});
var trainTypeDiv = 'type';
var trainNumDiv = 'trainNum';
var statsDiv = 'stats';

var typePicker = MYAPP.View.TypePicker({'divId': trainTypeDiv,
                                        'model': model});
model.addObserver(COMM.event.modelReady, typePicker);

var numPicker = MYAPP.View.NumPicker({'divId': trainNumDiv, 'model': model});
model.addObserver(COMM.event.modelReady, numPicker);
typePicker.addObserver(COMM.event.typeChanged, numPicker);

var trainStats = MYAPP.View.TrainStats({'divId': 'stats', 'model': model});
model.addObserver(COMM.event.modelReady, trainStats);
numPicker.addObserver(COMM.event.trainChanged, trainStats);

var searchTrain = MYAPP.View.SearchTrain({'model': model});
model.addObserver(COMM.event.modelReady, searchTrain);

var picker = MYAPP.View.TabView({'divId': '#menuPicker'});
picker.fillTabHeader(0, '1');
picker.fillTabContent(0, trainTypeDiv);
picker.fillTabHeader(1, '2');
picker.fillTabContent(1, trainNumDiv);
model.addObserver(COMM.event.modelReady, picker);

var eventDispatcher = COMM.Observer({});
eventDispatcher.trigger = function(eventName, params) {
    var img; // trainDescr = {};
    switch (eventName) {
        case COMM.event.typeChanged:
            img = "<img src='images/" + params.trainType + ".jpg' />";
            picker.fillTabHeader(0, img);
            picker.setTabFocus(1);
            picker.fillTabHeader(1, '-');
            break;
        case COMM.event.trainChanged:
            picker.fillTabHeader(1, params.trainId);
            picker.setTabFocus(-1);
            break;
    }
}

typePicker.addObserver(COMM.event.typeChanged, eventDispatcher);
numPicker.addObserver(COMM.event.trainChanged, eventDispatcher);

