var MYAPP = MYAPP || {};
MYAPP.View = MYAPP.View || {};

MYAPP.View.SearchTrain = function(proto) {
    var anchor, dataset, myModel, status, writeTable, that;
    anchor = proto.anchor;
    dataset = [];
    myModel = proto.model;
    status = "disabled";
    that = COMM.Observer(proto);

    writeTable = function () {
        var attributes, button, dataTd, dataTr, labels, table, tbody, th, thead, trHead;

        attributes = ['type', 'key', 'leaveTime', 'leaveStation', 'endStation',
                      'arriveTime'];
        labels = ['Treno', 'Op'];
        table = document.createElement('table');
        tbody = document.createElement('tbody');
        thead = document.createElement('thead');
        trHead = document.createElement('tr');


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
                dataTd.innerHTML += dataset[i][attributes[j]] + '&nbsp;';
            }
            dataTr.appendChild(dataTd);
            dataTd = document.createElement('td');
            button = document.createElement('input');
            button.setAttribute('data-num', dataset[i]['key']);
            button.setAttribute('data-type', dataset[i]['type']);
            button.setAttribute('data-from', dataset[i]['leaveStation']);
            button.setAttribute('data-to', dataset[i]['endStation']);
            button.setAttribute('data-leave', dataset[i]['leaveTime']);
            button.setAttribute('data-arrive', dataset[i]['arriveTime']);

            button.type = 'button';
            if (dataset[i]['isSurveyed'] === 'NOT_SURVEYED') {
                button.value = 'add';
                button.addEventListener('click', function () {
                    myModel.addSurvey(this.dataset,
                        function(res) {
                            alert(res);
                        });
                    });
            } else {
                button.value = 'view';
            }
            dataTd.appendChild(button);
            dataTr.appendChild(dataTd);
            tbody.appendChild(dataTr);
        }
        return table;
    }

    if (!proto.model) {
        console.log('SearchTrain, I need a model');
    }

    that.trigger = function(eventName, params) {
        if (eventName === COMM.event.modelReady) {
            status = 'collapsed';
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
        var button, container, form, formDiv, fromField, link, label, results,
        toField, timeRange, timeRangeId, timeRangeValue, timeRangeLabel;
        timeRangeId = ['a', 'b', 'c', 'd', 'e'];
        timeRangeValue = [1, 2, 3, 4, 5];
        timeRangeLabel = ['prima dell 6', '6-13', '13-18', '18-22', 'dopo le 22'];
        container = document.createElement('div');
        formDiv = document.createElement('div');
        form = document.createElement('form');

        container.setAttribute('id', anchor);
        container.setAttribute('style', "clear: left;");
        formDiv.style.display = 'none';
        formDiv.appendChild(form);
        fromField = document.createElement('input');
        fromField.type = 'text';
        toField = document.createElement('input');
        toField.type = 'text';
        form.appendChild(fromField);
        form.appendChild(toField);
        for(var i = 0; i < timeRangeId.length; ++i) {
            timeRange = document.createElement('input');
            timeRange.setAttribute('id', timeRangeId[i]);
            timeRange.type = 'radio';
            timeRange.name = 'timeRage';
            timeRange.value = timeRangeValue[i];
            if (i === 0) {
                timeRange.setAttribute('checked', 'checked');
            }
            label = document.createElement('label');
            label.innerHTML = timeRangeLabel[i];
            label.setAttribute('for', timeRangeId[i]);
            form.appendChild(timeRange);
            form.appendChild(label);
        }

        button = document.createElement('input');
        button.type = 'button';
        button.addEventListener('click', function () {
            var params = {}, radioObj = document.getElementsByName('timeRage');
            params = {'fromStation': fromField.value, 'toStation': toField.value,
                      'timeRange': 2};
            if(radioObj) {
                for(var i = 0; i < radioObj.length; i++) {
                        if (radioObj[i].checked) {
                            params.timeRange = radioObj[i].value;
                            break;
                        }
                }
            }

            myModel.trainLookUp(params, function(res) {
                res = res || [];
                status = 'showResults';
                that.update(res);
            });
        });
        form.appendChild(button);


        if (status === 'disabled') {
            return;
        }
        if (status === 'collapsed') {
            link = document.createElement('a');
            link.innerHTML = 'Cercalo <u>qui</u>';
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
            results =  document.querySelector('#results');
            //container.appendChild(COMM.writeTable(['Treno', 'Op'], dataset,
            //                      ['key', 'leaveTime', 'leaveStation', 'endStation', 'arriveTime', 'isSurveyed']));

            if (results) {
                while (results.hasChildNodes()) {
                    results.removeChild(results.lastChild);
                }
            } else {
                results = document.createElement('div');
                results.setAttribute('id', 'results');
                container.appendChild(results);
            }
            results.appendChild(writeTable());
        }
        document.querySelector('#search').appendChild(container);
    };
    that.draw();
    return that;
}
