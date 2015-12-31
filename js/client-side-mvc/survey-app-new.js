
var model = MYAPP.Model({});
var trainTypeDiv = 'type', trainNumDiv = 'trainNum', surveyDiv1 = 'survey',
surveyDiv2 = 'compare', surveyDiv3 = 'table_div', dateDiv = 'date';

var typePicker = MYAPP.View.TypePicker({'divId': trainTypeDiv,
                                        'model': model});
model.addObserver(COMM.event.modelReady, typePicker);

var numPicker = MYAPP.View.NumPicker({'divId': trainNumDiv, 'model': model});
model.addObserver(COMM.event.modelReady, numPicker);
typePicker.addObserver(COMM.event.typeChanged, numPicker);

var datePicker = MYAPP.View.DatePicker({'divId': dateDiv});
numPicker.addObserver(COMM.event.trainChanged, datePicker);

var surveys = MYAPP.View.Surveys({'divId': surveyDiv1, 'divId2': surveyDiv2,
                                  'divId3': surveyDiv3, 'model': model});
model.addObserver(COMM.event.modelReady, surveys);
datePicker.addObserver(COMM.event.dateChanged, surveys);

var readyDispatcher = COMM.DocReadyDispatcher({});
readyDispatcher.addObserver(COMM.event.docReady, typePicker);

var tabView = MYAPP.View.TabView({'divId': '#nav'});
tabView.fillTabHeader(0, COMM.lineIcon);
tabView.fillTabContent(0, trainTypeDiv);
tabView.fillTabHeader(1, COMM.trainIcon);
tabView.fillTabContent(1, trainNumDiv);
tabView.fillTabHeader(2, COMM.calendarIcon);
tabView.fillTabContent(2, dateDiv);
model.addObserver(COMM.event.modelReady, tabView);
tabView.addObserver(COMM.event.tabChanged, surveys);

var wizard = COMM.Observer({});
wizard.trigger = function(eventName, params) {
    var innerHTML;
    //surveys.hide();
    switch (eventName) {
        case COMM.event.typeChanged:
            innerHTML = COMM.lineIcon + "<img src='images/" + params.trainType + ".jpg' class='typeIcon'/>";
            tabView.fillTabHeader(0, innerHTML);
            tabView.fillTabHeader(1, '-');
            tabView.setTabFocus(1);
            break;
        case COMM.event.trainChanged:
            tabView.fillTabHeader(1, COMM.trainIcon + params.trainId);
            tabView.setTabFocus(2);
            break;
        case COMM.event.dateChanged:
            tabView.fillTabHeader(2, COMM.calendarIcon + params.selectedDate);
            tabView.setTabFocus(-1);
            break;
    }
}
typePicker.addObserver(COMM.event.typeChanged, wizard);
numPicker.addObserver(COMM.event.trainChanged, wizard);
datePicker.addObserver(COMM.event.dateChanged, wizard);
