var MYAPP = MYAPP || {};

MYAPP.Model = function(){
	this.trainList = [];
	this.observerList = [];
}

MYAPP.Model.prototype.ready = function() {
	console.log("Ready to be queried");
	for (var i = 0; i < this.observerList.length; i++) {
		this.observerList[i].update();
	}
};

MYAPP.Model.prototype.addObserver = function(obj) {
	//@todo check if already present.
	this.observerList.push(obj);
};

MYAPP.Model.prototype.getTrainList = function(callback) {
	if (this.trainList.length == 0) {
	    gapi.client.discover.trains.listSurveyedTrain().execute(
		function(resp) {
			if (!resp.code) {
				resp.items = resp.items || [];
				this.trainList = resp.items;
				callback(this.trainList);
			}
		});
	} else {
		callback(this.trainList);
	}
};

MYAPP.Model.prototype.getTrainStats = function(trainId, filter, callback) {
	var params = {'trainid': trainId, 'dayFilter': 'all'};
	if (filter !== 'all' && filter !== 'dayOff' && filter !== 'workDay') {
		console.log("Model: Wrong filter passed.");
	} else {
		params.dayFilter = filter;
	}
	gapi.client.statistics.trains.listStop(params).execute(
		function(resp) {
			if (!resp.code) {
				resp.items = resp.items || [];
				callback(resp.items);
			}
	      });
};

var myModel = new MYAPP.Model();
