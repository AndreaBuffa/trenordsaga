var MYAPP = MYAPP || {};
MYAPP.View = MYAPP.View || {};

MYAPP.View.NumPicker = function(proto) {
    var myModel, status, that;
    myModel = proto.model;
    status = "loading";
    that = COMM.Notifier(COMM.Observer(COMM.State(proto)));

    that.trigger = function(eventName, _params) {
        switch(eventName) {
            case COMM.event.modelReady:
            case COMM.event.typeChanged:
                this.update(_params);
            break;
            case COMM.event.tabChanged:
                 this.update();
        }
    };

    that.update = function(_params) {
        if (_params) {
            that.setState(_params);
        }
        myModel.getTrainList(that.getState(), function(trainList) {
            trainList = trainList || [];
            status = "ready";
            that.draw(trainList);
        });
    };

    that.draw = function(trainList) {
        var container = document.querySelector('#' + proto.divId), currRailwayType = '',
        from = '', linkControl, label, table, td, th1, thead, to = '', tr,
        trHead, train, trainListDiv;

        if (container) {
            while (container.hasChildNodes()) {
                container.removeChild(container.lastChild);
            }
        } else {
            container = document.createElement('div');
            container.setAttribute('id', proto.divId);
            document.querySelector('#container').appendChild(container);
        }
        if (status === "loading") {
            container.innerHTML = "Loading....";
            return;
        }
        if (trainList.length === 0) {
            return;
        }
        label = document.createElement('div');
        label.innerHTML = '<header class="major"><h2>{{ nls.choose_train_num }}</h2></header';
        container.appendChild(label);

        for (var i = 0; i < trainList.length; i++) {
            train = trainList[i];
            if (currRailwayType != train.type) {
                currRailwayType = train.type;
                trainListDiv = document.createElement('div');
                trainListDiv.id = currRailwayType + 'trainList';
                trainListDiv.classList.add('table-wrapper');
            }
            if (from != train.leaveStation || to != train.endStation) {
                from = train.leaveStation;
                to = train.endStation;

                table = document.createElement('table');
                thead = document.createElement('thead');
                trHead = document.createElement('tr');
                th1 = document.createElement('th');
                th1.innerHTML = from + ' - ' + to;
                th1.setAttribute('colspan', '3');
                trHead.appendChild(th1);
                thead.appendChild(trHead);
                table.appendChild(thead);
                trainListDiv.appendChild(table);
                container.appendChild(trainListDiv);
            }
            linkControl = document.createElement('a');
            linkControl.setAttribute('id', train.trainId);
            linkControl.setAttribute('data-traintype', train.type);
            linkControl.setAttribute('data-surveyedfrom', train.surveyedFrom);
            linkControl.setAttribute('data-leavetime', train.leaveTime);
            linkControl.addEventListener('click', function () {
                    that.notify(COMM.event.trainChanged, {'trainId': this.id,
                        'trainType': this.dataset.traintype,
                        'leaveTime': this.dataset.leavetime,
                        'dayFilter': 'all',
                        'surveyedFrom': this.dataset.surveyedfrom});
                });

            tr = document.createElement('tr');
            tr.setAttribute('class', 'trainTr');
            tr.innerHTML = ['<td name="time"><b>', train.leaveTime, '</b></td>',
                            '<td name="sep">num:</td>', '<td>', train.trainId,
                            '</td>'].join("");
            table.appendChild(tr);
            tr = document.createElement('tr');
            tr.setAttribute('class', 'trainTr');
            td = document.createElement('td');
            tr.appendChild(td);
            td = document.createElement('td');
            td.setAttribute('name', 'sep');
            td.innerHTML = 'da:';
            tr.appendChild(td);
            td = document.createElement('td');
            linkControl.innerHTML = train.leaveStation;
            td.appendChild(linkControl);
            tr.appendChild(td);
            table.appendChild(tr);

            tr = document.createElement('tr');
            tr.setAttribute('class', 'trainTr');
            td = document.createElement('td');
            tr.appendChild(td);
            td = document.createElement('td');
            td.setAttribute('name', 'sep');
            td.innerHTML = 'a:';
            tr.appendChild(td);
            td = document.createElement('td');
            var linkControl2 = linkControl.cloneNode(true);

            linkControl2.addEventListener('click', function () {
                    that.notify(COMM.event.trainChanged, {'trainId': this.id,
                        'trainType': this.dataset.traintype,
                        'leaveTime': this.dataset.leavetime,
                        'dayFilter': 'all',
                        'surveyedFrom': this.dataset.surveyedfrom});
                });

            linkControl2.innerHTML = [train.endStation, ' (', train.arriveTime,
                                      ')'].join("");
            td.appendChild(linkControl2);
            tr.appendChild(td);
            table.appendChild(tr);
            tr = document.createElement('tr');
            tr.setAttribute('class', 'trainTrSep');
            table.appendChild(tr);

/*            tr.innerHTML = ['<table class="reset"><tr><td name="time"><b>', train.leaveTime, '</b></td>',
                         '<td name="sep">num:</td>', '<td>', train.trainId, '</td></tr>',
                         '<tr><td></td><td name="sep">da:</td><td>', train.leaveStation, '&nbsp;</td></tr>',
                         '<tr><td></td><td name="sep">a:</td><td>', train.endStation,
                         ' (', train.arriveTime,
                          ')', '</td></tr>', '</table>'].join("");*/

/*          var linkDiv = document.createElement('div');
            linkDiv.classList.add('row');
            linkDiv.appendChild(linkControl);*/
        }
    };

    return that;
};
