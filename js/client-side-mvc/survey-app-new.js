
var model = MYAPP.Model({});
var trainTypeDiv = 'type';
var trainNumDiv = 'trainNum';
var surveyDiv = 'survey';
var dateDiv = 'datepicker';

var typePicker = MYAPP.View.TypePicker({'divId': trainTypeDiv,
                                        'model': model});
model.addObserver(COMM.event.modelReady, typePicker);

var numPicker = MYAPP.View.NumPicker({'divId': trainNumDiv, 'model': model});
model.addObserver(COMM.event.modelReady, numPicker);
typePicker.addObserver(COMM.event.typeChanged, numPicker);

var datePicker = MYAPP.View.DatePicker({'divId': dateDiv});
numPicker.addObserver(COMM.event.trainChanged, datePicker);

var surveys = MYAPP.View.Surveys({'divId': surveyDiv, 'model': model});
model.addObserver(COMM.event.modelReady, surveys);

var wizard = MYAPP.View.TabView({'divId': '#menuPicker'});
wizard.fillTabHeader(0, '1');
wizard.fillTabContent(0, trainTypeDiv);
wizard.fillTabHeader(1, '2');
wizard.fillTabContent(1, trainNumDiv);
wizard.fillTabHeader(2, '3');
wizard.fillTabContent(2, dateDiv);
model.addObserver(COMM.event.modelReady, wizard);


var eventDispatcher = COMM.Observer({});
eventDispatcher.trigger = function(eventName, params) {
    var img;
    switch (eventName) {
        case COMM.event.typeChanged:
            img = "<img src='images/" + params.trainType + ".jpg' />";
            wizard.fillTabHeader(0, img);
            wizard.setTabFocus(1);
            wizard.fillTabHeader(1, '-');
            break;
        case COMM.event.trainChanged:
            wizard.fillTabHeader(1, params.trainId);
            wizard.setTabFocus(2);
            break;
        case COMM.event.dateChanged:
            wizard.fillTabHeader(2, params.selectedDate);
            wizard.setTabFocus(-1);
            break;
    }
}
typePicker.addObserver(COMM.event.typeChanged, eventDispatcher);
numPicker.addObserver(COMM.event.trainChanged, eventDispatcher);
datePicker.addObserver(COMM.event.dateChanged, eventDispatcher);
