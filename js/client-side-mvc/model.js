var MYAPP = MYAPP || {};

MYAPP.Model = function() {
    var currTrainId, status = 'loading', that, trainList = [];
    that = COMM.Observer(COMM.Notifier({}));

    that.ready = function () {
        console.log("Model Ready");
        status = 'ready';
        that.notify(COMM.event.modelReady);
    };

    that.trigger = function(eventName, params) {
		switch(eventName) {
			case COMM.event.trainChanged:
				currTrainId = params.trainId;
			break;
		}
    };

    that.getTrainList = function(params, callback) {
        if (status !== 'ready')
            return;
        if (trainList.length == 0) {
            gapi.client.discover.trains.listSurveyedTrain().execute(
                function(resp) {
                    if (!resp.code) {
                        resp.items = resp.items || [];
                        trainList = resp.items;
                        callback(trainList);
                    }
                });
        } else {
            if (params.trainType) {
                var tmp = new Array();
                for (var i = 0; i < trainList.length; i++) {
                    if (params.trainType === trainList[i].type) {
                        tmp.push(trainList[i]);
                    }
                }
                callback(tmp);
            } else {
                callback(trainList);
            }
        }
    };

    that.getTrainDescr = function(trainId) {
        for(var i = 0; i < trainList.length; i++) {
            if (trainList[i].trainId === trainId) {
                return trainList[i];
            }
        }
        return null;
    }

    that.getTrainStats = function(trainId, filter, callback) {
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

    that.trainLookUp = function(params, callback) {
        var date = new Date(), formatDate;
        formatDate = [date.getFullYear(), '-', date.getMonth() + 1,
                      '-', date.getDate()].join("");
        params.when = formatDate;

        gapi.client.discover.trains.searchFromTo(params).execute(
            function(resp) {
                if (!resp.code) {
                    resp.items = resp.items || [];
                    callback(resp.items);
                }
        });
    };

    that.addSurvey = function(params, callback) {

        var args = {'num': params.num, 'trainType': params.type,
                      'fromStation': params.from,
                      'toStation': params.to, 'leave': params.leave,
                      'arrive': params.arrive};

        gapi.client.discover.trains.addSurvey(args).execute(function(resp) {
            //@todo check the return code
            if (!resp.code) {
                callback(true);
            }
        });
    };

    that.getSurveyGraphData = function(params, callback) {
        var date = new Array();
        // some params name translations
        params.trainid = params.trainId;
        date = params.selectedDate.split('-');
        if (date.length !== 3) {
            console.log("Model: wrong date passed");
            return;
        }
        params.year = date[0];
        params.month = date[1];
        params.day = date[2];
        gapi.client.schedule.trains.getSurveyGraphData(params).execute(
            function(resp) {
                var columnChartData = {}, lineChartData = {};
                //@todo check the return code
                if (!resp.code) {
                    if (resp.scheduled_real) {
                        lineChartData = JSON.parse(resp.scheduled_real);
                        columnChartData = JSON.parse(resp.real_median);
                    }
                    callback(lineChartData, columnChartData);
                }
        });
    }

    that.getStatsGraphData = function(trainId, callback) {
        var params = {'trainid': trainId};
        gapi.client.statistics.trains.getStatsGraphData(params).execute(
            function(resp) {
                var chartData = {};
                //@todo check the return code
                if (!resp.code) {
                    if (resp.median) {
                        chartData = JSON.parse(resp.median);
                    }
                    callback(chartData);
                }
            }
        );
    }

    that.getSurveyDataSource = function(params, callback) {
        gapi.client.discover.trains.getDataSource(params).execute(
            function(resp) {
                //@todo check the return code
                if (!resp.code) {
                    resp.items = resp.items || [];
                    //x = x.replace(/\\"/g, '"');
                    callback(resp.items);
                }
        });
    }

    that.getCurrentTrainId = function() {
        return currTrainId;
    }

    return that;
}
