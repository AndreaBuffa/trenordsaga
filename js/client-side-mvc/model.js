var MYAPP = MYAPP || {};

MYAPP.Model = function() {
    var that = COMM.Notifier({});
    var trainList = [];
    that.ready = function () {
        that.notify(COMM.event.modelReady);
    };

    that.getTrainList = function(callback) {
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
            callback(trainList);
        }
    };

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

    that.trainLookUp = function(fromStation, to, callback) {
        var params = {'fromStation': fromStation, 'toStation': to,
                      'when': new Date(), 'timeRange': 3};

        gapi.client.discover.trains.searchFromTo(params).execute(
            function(resp) {
                if (!resp.code) {
                    resp.items = resp.items || [];
                    callback(resp.items);
                }
            });
    };

    return that;
}
