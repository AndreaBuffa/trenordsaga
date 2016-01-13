var MYAPP = MYAPP || {};
MYAPP.View = MYAPP.View || {};

MYAPP.View.NumPicker = function(proto) {
/*	@todo check state
*/
    var anchor, myModel, currType, status, that;
    anchor = proto.anchor;
    myModel = proto.model;
    status = "loading";
    that = COMM.Notifier(COMM.Observer(proto));

    that.trigger = function(eventName, params) {
        switch(eventName) {
            case COMM.event.modelReady:
                status = "ready";
                return;
            case COMM.event.typeChanged:
                if (status !== "ready") {
                    return;
                }
                currType = params.trainType;
        }
        this.update();
    };

    that.update = function() {
        myModel.getTrainList({'trainType': currType}, function(trainList) {
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
                trHead.appendChild(th1);
                thead.appendChild(trHead);
                table.appendChild(thead);
                trainListDiv.appendChild(table);
                container.appendChild(trainListDiv);
                //
            }
            linkControl = document.createElement('a');
            linkControl.setAttribute('id', train.trainId);
            linkControl.setAttribute('data-type', train.type);
            linkControl.setAttribute('data-surveyedfrom', train.surveyedFrom);
            linkControl.setAttribute('data-leavetime', train.leaveTime);
            linkControl.addEventListener('click', function () {
                    that.notify(COMM.event.trainChanged, {'trainId': this.id,
                        'type': this.dataset.type,
                        'leaveTime': this.dataset.leavetime,
                        'dayFilter': 'all',
                        'surveyedFrom': this.dataset.surveyedfrom});
                });
            linkControl.innerHTML = ['<b>', train.leaveTime, '</b>',
                         ' - ',
                         train.trainId, '&nbsp;',
                         train.leaveStation, '&nbsp;',
                         train.endStation,
                         ' (', train.arriveTime,
                          ')'].join("");

/*          var linkDiv = document.createElement('div');
            linkDiv.classList.add('row');
            linkDiv.appendChild(linkControl);*/
            tr = document.createElement('tr');
            td = document.createElement('td');
            td.appendChild(linkControl);
            tr.appendChild(td);
            table.appendChild(tr);
        }
    };

    return that;
}
