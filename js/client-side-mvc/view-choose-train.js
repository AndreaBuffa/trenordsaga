var MYAPP = MYAPP || {};
MYAPP.View = MYAPP.View || {};

MYAPP.View.TrainSelector = function(proto) {
/*	@todo check state
*/
    var anchor, myModel, status, that;
    anchor = proto.anchor;
    myModel = proto.model;
    status = "loading";
    that = COMM.Observer(proto);
    that = COMM.Notifier(that);

    that.trigger = function(eventName, params) {
        this.update();
    };

    that.update = function() {
        myModel.getTrainList(function(trainList) {
            trainList = trainList || [];
/*			trainList.sort(function(a, b) {
				var number1 = a.type.match(/(\d+)$/);
				var number2 = b.type.match(/(\d+)$/);
				if (number1 == null) {
					if (number2 == null) {
						return 0;
					} else {
						return -1;
					}
				} else {
					if (number2 == null) {
						return 1;
					} else {
						return parseInt(number1[0]) - parseInt(number2[0]);
					}
				}
			});*/
            status = "ready";
            that.draw(trainList);
        });
    };

    that.draw = function(trainList) {
        var container = document.querySelector('#trainSelector'), img,
        currRailwayType = '', from = '', linkControl, railwayDiv, railwayLink,
        searchLink, table, td, th1, thead, to = '', tr, trHead, train, trainList,
        trainListDiv;

        if (container) {
            while (container.hasChildNodes()) {
                container.removeChild(container.lastChild);
            }
        } else {
            container = document.createElement('div');
            container.setAttribute('id', 'trainSelector');
            document.querySelector('#container').appendChild(container);
        }
        if (status === "loading") {
            container.innerHTML = "Loading....";
            return;
        }

        for (var i = 0; i < trainList.length; i++) {
            train = trainList[i];
            if (currRailwayType != train.type) {
                searchLink = document.createElement('a');
                searchLink.innerHTML = "Se non lo trovi cercalo qui";
                searchLink.href = '#' + anchor;
                if (trainListDiv)
                    trainListDiv.appendChild(searchLink);

                currRailwayType = train.type;
                railwayDiv = document.createElement('div');
                railwayDiv.classList.add('trainType');
                railwayLink = document.createElement('a');
                railwayLink.id = currRailwayType;
                img = document.createElement('img');
                img.src = 'images/' + currRailwayType + '.jpg';
                railwayLink.appendChild(img);
                railwayLink.addEventListener('click', function() {
                    trainList = document.querySelectorAll('[id$=trainList]');
                    for(var i=0; i < trainList.length; i++) {
                        if (trainList[i].id === this.id + 'trainList') {
                            trainList[i].style.display = 'block';
                            trainList[i].style.clear = 'left';
                        } else {
                            trainList[i].style.display = 'none';
                        }
                    }
                });
                railwayDiv.appendChild(railwayLink);
                container.appendChild(railwayDiv);
                trainListDiv = document.createElement('div');
                trainListDiv.id = currRailwayType + 'trainList';
                trainListDiv.classList.add('table-wrapper');
                trainListDiv.style.display = 'none';
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
            linkControl.setAttribute('data-surveyedfrom', train.surveyedFrom);
            linkControl.addEventListener('click', function () {
                    that.onClick({'trainId': this.id,
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

    that.onClick = function(newTrain) {
        this.notify(COMM.event.trainChanged, newTrain);
    };

    return that;
}
