"use strict";
var COMM = COMM || {};

COMM.isArray = function(myArray) {
    if (myArray) {
        return myArray.constructor.toString().indexOf("Array") > -1;
    }
    return false;
};

COMM.Observer = function(spec) {
    var that = {};
    that.trigger = function(eventName, params) {
        console.log("Implement me...");
    };
    return that;
};

COMM.Notifier = function() {
    var that = {};
    that.observerList = {};
    that.addObserver = function(eventName, observer) {
        //check observer type
        if (COMM.isArray(that.observerList[eventName])) {
            that.observerList[eventName].push(observer);
        } else {
            that.observerList[eventName] = [observer];
        }
    };
    that.notify = function(eventName, params) {
        if (COMM.isArray(that.observerList[eventName])) {
            for (var i = 0; i < that.observerList[eventName].length; i++) {
                that.observerList[eventName][i].trigger(eventName, params);
            }
        } else {
            console.log("No observer registered to this event:" + eventName);
        }
    };
    return that;
};

COMM.event = {
    modelReady: "modelReady",
    trainChanged: "trainChanged"
};
