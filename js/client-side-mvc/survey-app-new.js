
var model = MYAPP.Model({});
var trainTypeDiv = 'type', trainNumDiv = 'trainNum', surveyDiv1 = 'survey',
surveyDiv2 = 'compare', dateDiv = 'date';

var typePicker = MYAPP.View.TypePicker({'divId': trainTypeDiv,
                                        'model': model});
model.addObserver(COMM.event.modelReady, typePicker);

var numPicker = MYAPP.View.NumPicker({'divId': trainNumDiv, 'model': model});
model.addObserver(COMM.event.modelReady, numPicker);
typePicker.addObserver(COMM.event.typeChanged, numPicker);

var datePicker = MYAPP.View.DatePicker({'divId': dateDiv});
numPicker.addObserver(COMM.event.trainChanged, datePicker);

var surveys = MYAPP.View.Surveys({'divId': surveyDiv1, 'divId2': surveyDiv2,
                                  'model': model});
model.addObserver(COMM.event.modelReady, surveys);
datePicker.addObserver(COMM.event.dateChanged, surveys);

var wizard = MYAPP.View.TabView({'divId': '#nav'});
wizard.fillTabHeader(0, COMM.lineIcon);
wizard.fillTabContent(0, trainTypeDiv);
wizard.fillTabHeader(1, COMM.trainIcon);
wizard.fillTabContent(1, trainNumDiv);
wizard.fillTabHeader(2, COMM.calendarIcon);
wizard.fillTabContent(2, dateDiv);
model.addObserver(COMM.event.modelReady, wizard);


var eventDispatcher = COMM.Observer({});
eventDispatcher.trigger = function(eventName, params) {
    var innerHTML;
    switch (eventName) {
        case COMM.event.typeChanged:
            innerHTML = COMM.lineIcon + "<img src='images/" + params.trainType + ".jpg' />";
            wizard.fillTabHeader(0, innerHTML);
            wizard.fillTabHeader(1, '-');
            wizard.setTabFocus(1);
            break;
        case COMM.event.trainChanged:
            wizard.fillTabHeader(1, COMM.trainIcon + params.trainId);
            wizard.setTabFocus(2);
            break;
        case COMM.event.dateChanged:
            wizard.fillTabHeader(2, COMM.calendarIcon + params.selectedDate);
            wizard.setTabFocus(-1);
            break;
    }
}
typePicker.addObserver(COMM.event.typeChanged, eventDispatcher);
numPicker.addObserver(COMM.event.trainChanged, eventDispatcher);
datePicker.addObserver(COMM.event.dateChanged, eventDispatcher);
