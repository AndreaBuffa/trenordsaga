
var model = MYAPP.Model({});
var trainTypeDiv = 'type', trainNumDiv = 'trainNum', dateDiv = 'date',
searchDiv = 'search';
var divList = ['trend', 'survey', 'compareHeader', 'compare', 'compareTableHeader',
'table_div', 'nosurvey'];
var date = COMM.getYesterdayDate();
var mediator = (function() {
    var currSettings = {}, that = {};
    currSettings.selectedDate = date;
    that = COMM.Notifier(COMM.Observer(that));
    that.trigger = function(eventName, param) {
        switch(eventName) {
            case COMM.event.typeChanged:
                currSettings.trainType = param.trainType;
                this.notify(COMM.event.typeChanged, currSettings);
            break;
            case COMM.event.trainChanged:
                currSettings.trainId = param.trainId;
                this.notify(COMM.event.trainChanged, currSettings);
            break;
            case COMM.event.dateChanged:
                currSettings.selectedDate = param.selectedDate;
                this.notify(COMM.event.dateChanged, currSettings);
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
model.addObserver(COMM.event.modelReady, surveys);

var readyDispatcher = COMM.DocReadyDispatcher({});
readyDispatcher.addObserver(COMM.event.docReady, typePicker);

var scrollUpNotifier = COMM.ScrollUpDispatcher({});
var searchTrain = MYAPP.View.Search({'divId': searchDiv});
scrollUpNotifier.addObserver(COMM.event.scrollUp, searchTrain);
readyDispatcher.addObserver(COMM.event.docReady, searchTrain);
model.addObserver(COMM.event.modelReady, searchTrain);

var tabView = MYAPP.View.TabView({'divId': '#nav'});
readyDispatcher.addObserver(COMM.event.docReady, tabView);

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
            tabView.fillTabHeader(2, liBuilder.getCalendarLi(COMM.toISOString(params.selectedDate)));
            tabView.setTabFocus(-1);
            break;
    }
}
typePicker.addObserver(COMM.event.typeChanged, wizard);
numPicker.addObserver(COMM.event.trainChanged, wizard);
datePicker.addObserver(COMM.event.dateChanged, wizard);
if (urlParams.trainId) {
    wizard.trigger(COMM.event.typeChanged, urlParams);
    wizard.trigger(COMM.event.trainChanged, urlParams);
    wizard.trigger(COMM.event.dateChanged, urlParams);
    typePicker.setState(urlParams);
    typePicker.notify(COMM.event.typeChanged, urlParams);
    numPicker.setState(urlParams);
    numPicker.notify(COMM.event.trainChanged, urlParams);
    datePicker.setState(urlParams);
    datePicker.notify(COMM.event.dateChanged, urlParams);
}
