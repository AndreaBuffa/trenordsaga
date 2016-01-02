
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

var picker = MYAPP.View.TabView({'divId': '#nav'});
picker.fillTabHeader(0, '');
picker.fillTabContent(0, trainTypeDiv);
picker.fillTabHeader(1, '');
picker.fillTabContent(1, trainNumDiv);
model.addObserver(COMM.event.modelReady, picker);
picker.addObserver(COMM.event.tabChanged, trainStats);

var eventDispatcher = COMM.Observer({});
var liBuilder = COMM.MenuLiBuilder({});
eventDispatcher.trigger = function(eventName, params) {
    switch (eventName) {
        case COMM.event.typeChanged:
            picker.fillTabHeader(0, liBuilder.getTypeLi(params.trainType));
            picker.fillTabHeader(1, '-');
            picker.setTabFocus(1);
            break;
        case COMM.event.trainChanged:
            picker.fillTabHeader(1, liBuilder.getTrainNumLi(params.trainId));
            picker.setTabFocus(-1);
            break;
    }
}

typePicker.addObserver(COMM.event.typeChanged, eventDispatcher);
numPicker.addObserver(COMM.event.trainChanged, eventDispatcher);

