
var model = MYAPP.Model({});
var trainTypeDiv = 'type', trainNumDiv = 'trainNum', dateDiv = 'date',
searchDiv = 'search';
var divList = ['trend', 'survey', 'compareHeader', 'compare', 'compareTableHeader',
'table_div', 'nosurvey'];


var typePicker = MYAPP.View.TypePicker({'divId': trainTypeDiv,
                                        'model': model});
model.addObserver(COMM.event.modelReady, typePicker);

var numPicker = MYAPP.View.NumPicker({'divId': trainNumDiv, 'model': model});
model.addObserver(COMM.event.modelReady, numPicker);
typePicker.addObserver(COMM.event.typeChanged, numPicker);

var datePicker = MYAPP.View.DatePicker({'divId': dateDiv});
numPicker.addObserver(COMM.event.trainChanged, datePicker);

var surveys = MYAPP.View.Surveys({'divList': divList, 'model': model});
datePicker.addObserver(COMM.event.dateChanged, surveys);

var readyDispatcher = COMM.DocReadyDispatcher({});
readyDispatcher.addObserver(COMM.event.docReady, typePicker);

var scrollUpNotifier = COMM.ScrollUpDispatcher({});
var searchTrain = MYAPP.View.Search({'divId': searchDiv});
scrollUpNotifier.addObserver(COMM.event.scrollUp, searchTrain);
readyDispatcher.addObserver(COMM.event.docReady, searchTrain);
model.addObserver(COMM.event.modelReady, searchTrain);

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
var liBuilder = COMM.MenuLiBuilder({});
wizard.trigger = function(eventName, params) {
    var innerHTML;
    switch (eventName) {
        case COMM.event.typeChanged:
            innerHTML = liBuilder.getTypeLi(params.trainType);
            tabView.fillTabHeader(0, innerHTML);
            tabView.fillTabHeader(1, '-');
            tabView.setTabFocus(1);
            break;
        case COMM.event.trainChanged:
            tabView.fillTabHeader(1, liBuilder.getTrainNumLi(params.trainId));
            tabView.setTabFocus(2);
            break;
        case COMM.event.dateChanged:
            tabView.fillTabHeader(2, liBuilder.getCalendarLi(params.selectedDate));
            tabView.setTabFocus(-1);
            break;
    }
}
typePicker.addObserver(COMM.event.typeChanged, wizard);
numPicker.addObserver(COMM.event.trainChanged, wizard);
datePicker.addObserver(COMM.event.dateChanged, wizard);
