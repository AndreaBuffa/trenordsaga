var MYAPP = MYAPP || {};
MYAPP.View = MYAPP.View || {};

MYAPP.View.SearchTrain = function(proto) {
    var anchor = proto.anchor;
    var dataset = [];
    var myModel = proto.model;
    var status = "disabled";
    var that = COMM.Observer(proto);
    var writeTable = function () {
        var attributes = ['key', 'leaveTime', 'leaveStation', 'endStation',
                          'arriveTime'];
        var button;
        var dataTd, dataTr;
        var labels = ['Treno', 'Op'];
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
            dataTd = document.createElement('td');
            for (var j = 0; j < attributes.length; j++) {
                dataTd.innerHTML += dataset[i][attributes[j]];
            }
            dataTr.appendChild(dataTd);
            dataTd = document.createElement('td');
            button = document.createElement('input');
            button.type = 'button';
            button.value = dataset[i]['isSurveyed'] === 'NOT_SURVEYED' ? 'add' : 'view';
            button.addEventListener('click', function () {
                /*myModel.trainLookUp(fromField.value, toField.value,
                    function(res) {
                        res = res || [];
                        status = "showResults";
                        that.update(res);
                    });
                */
            });
            dataTd.appendChild(button);
            dataTr.appendChild(dataTd);
            tbody.appendChild(dataTr);
        }
        return table;
    }

    if (!proto.model) {
        console.log("SearchTrain, I need a model");
    }

    if (!proto.container) {
        console.log("SearchTrain, I need a div container");
    }

    that.trigger = function(eventName, params) {
        if (eventName === COMM.event.modelReady) {
            status = "collapsed";
            this.update();
        } else {
            log.console("Not listening to " + eventName);
        }
    };

    that.update = function (data) {
        dataset = data;
        this.draw();
    };

    that.draw = function () {
        var container = document.createElement('div');
        var formDiv = document.createElement('div');
        var form = document.createElement('form');

        container.setAttribute('id', anchor);
        container.setAttribute('style', "clear: left;");
        formDiv.style.display = 'none';
        formDiv.appendChild(form);
        var fromField = document.createElement('input');
        fromField.type = 'text';
        var toField = document.createElement('input');
        toField.type = 'text';
        form.appendChild(fromField);
        form.appendChild(toField);
        var button = document.createElement('input');
        button.type = 'button';
        button.addEventListener('click', function () {
            myModel.trainLookUp(fromField.value, toField.value, function(res) {
                res = res || [];
                status = "showResults";
                that.update(res);
            });
        });
        form.appendChild(button);


        if (status === 'disabled') {
            return;
        }
        if (status === "collapsed") {
            var link = document.createElement('a');
            link.innerHTML = "Cercalo <u>qui</u>";
            link.addEventListener('click', function () {
                    if (formDiv.style.display === 'none') {
                        formDiv.style.display = 'block';
                    } else {
                        formDiv.style.display = 'none';
                    }
                });
            container.appendChild(link);
            container.appendChild(formDiv);
        }
        if (status === "showResults") {
            //container.appendChild(COMM.writeTable(['Treno', 'Op'], dataset,
            //                      ['key', 'leaveTime', 'leaveStation', 'endStation', 'arriveTime', 'isSurveyed']));
            container.appendChild(writeTable());
        }
        document.querySelector('#container').appendChild(container);
    };
    that.draw();
    return that;
}
