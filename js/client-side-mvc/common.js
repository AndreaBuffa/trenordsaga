"use strict";
var COMM = COMM || {};

COMM.isArray = function(myArray) {
    if (myArray) {
        return myArray.constructor.toString().indexOf("Array") > -1;
    }
    return false;
};

COMM.Observer = function(that) {
    if (!that) {
        console.log("that observer is NULL");
        return;
    }
    that.trigger = function(eventName, params) {
        console.log("Implement me...");
    };
    return that;
};

COMM.Notifier = function (that) {
    if (!that) {
        console.log("that Notifier is NULL");
        return;
    }
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
    typeChanged: "typeChanged",
    trainChanged: "trainChanged",
    dateChanged: "dateChanged"
};

COMM.writeTable = function(labels, dataset, attributes) {
    var dataTd, dataTr;
    var table = document.createElement('table');
    var tbody = document.createElement('tbody');
    var th;
    var thead = document.createElement('thead');
    var trHead = document.createElement('tr');

    for (var i = 0; i < labels.length; i++) {
        th = document.createElement('th');
        th.innerHTML = labels[i];
        trHead.appendChild(th);
    }
    thead.appendChild(trHead);
    table.appendChild(thead);
    table.appendChild(tbody);
    for (var i = 0; i < dataset.length; i++) {
        dataTr = document.createElement('tr');
        for (var j = 0; j < attributes.length; j++) {
            dataTd = document.createElement('td');
            dataTd.innerHTML += dataset[i][attributes[j]];
            dataTr.appendChild(dataTd);
        }
        tbody.appendChild(dataTr);
    }
    return table;
};
