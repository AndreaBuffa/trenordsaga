var MYAPP = MYAPP || {};

MYAPP.Model = function() {
    var that = COMM.Notifier({}), trainList = [];

    that.ready = function () {
        console.log("Model Ready");
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

        var params = {'num': params.num, 'trainType': params.type,
                      'fromStation': params.from,
                      'toStation': params.to, 'leave': params.leave,
                      'arrive': params.arrive};

        gapi.client.discover.trains.addSurvey(params).execute(function(resp) {
            //@todo check the return code
            if (!resp.code) {
                callback(true);
            }
        });
    };

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

    return that;
}
