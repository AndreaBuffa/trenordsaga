
var model = MYAPP.Model({});
var trainTypeDiv = 'type', trainNumDiv = 'trainNum', dateDiv = 'date',
searchDiv = 'search';
var divList = ['trend', 'survey', 'compareHeader', 'compare', 'compareTableHeader',
'table_div', 'nosurvey'];
var date = COMM.getYesterdayDate();
var mediator = (function() {
    var that = {};

    that = COMM.Notifier(COMM.Observer(that));
    that.trigger = function(eventName, param) {
        switch(eventName) {
            case COMM.event.typeChanged:
                param.selectedDate = date;
                this.notify(COMM.event.typeChanged, param);
            break;
            case COMM.event.trainChanged:
                param.selectedDate = date;
                this.notify(COMM.event.trainChanged, param);
            break;
            case COMM.event.dateChanged:
                date = param.selectedDate;
                this.notify(COMM.event.dateChanged, param);
            break;
        }
    }
    return that;
}());

var typePicker = MYAPP.View.TypePicker({'divId': trainTypeDiv,
                                        'model': model});
model.addObserver(COMM.event.modelReady, typePicker);
typePicker.addObserver(COMM.event.typeChanged, mediator);

var numPicker = MYAPP.View.NumPicker({'divId': trainNumDiv, 'model': model});
model.addObserver(COMM.event.modelReady, numPicker);
mediator.addObserver(COMM.event.typeChanged, numPicker);
numPicker.addObserver(COMM.event.trainChanged, mediator);

var datePicker = MYAPP.View.DatePicker({'divId': dateDiv});
datePicker.addObserver(COMM.event.dateChanged, mediator);
mediator.addObserver(COMM.event.trainChanged, datePicker);

var surveys = MYAPP.View.Surveys({'divList': divList, 'model': model});
mediator.addObserver(COMM.event.trainChanged, surveys);
mediator.addObserver(COMM.event.dateChanged, surveys);

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
var liBuilder = COMM.MenuLiBuilder({});
tabView.fillTabHeader(2, liBuilder.getCalendarLi(COMM.toISOString(date)));
tabView.fillTabContent(2, dateDiv);
model.addObserver(COMM.event.modelReady, tabView);
tabView.addObserver(COMM.event.tabChanged, surveys);

var wizard = COMM.Observer({});
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
            tabView.setTabFocus(-1);
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
