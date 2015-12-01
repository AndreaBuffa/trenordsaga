
var model = MYAPP.Model({});
var trainTypeDiv = 'type';
var trainNumDiv = 'trainNum';
var surveyDiv = 'survey';

var typePicker = MYAPP.View.TypePicker({'divId': trainTypeDiv,
                                        'model': model,
                                        'anchor': '#search'});
model.addObserver(COMM.event.modelReady, typePicker);

var numPicker = MYAPP.View.NumPicker({'divId': trainNumDiv, 'model': model});
model.addObserver(COMM.event.modelReady, numPicker);
typePicker.addObserver(COMM.event.typeChanged, numPicker);

var surveys = MYAPP.View.Surveys({'divId': surveyDiv, 'model': model});
model.addObserver(COMM.event.modelReady, surveys);
