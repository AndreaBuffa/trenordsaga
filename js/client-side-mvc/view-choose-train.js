var MYAPP = MYAPP || {};
MYAPP.View = MYAPP.View || {};

MYAPP.View.TrainSelector = function(proto) {
/*	@todo check state
*/
    var myModel = proto.model;
	var status = "loading";
	var that = COMM.Observer(proto);
	that = COMM.Notifier(that);

	that.trigger = function(eventName, params) {
		this.update();
	}

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
	}

	that.draw = function(trainList) {
        var container = document.querySelector('#trainSelector');
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
        var currRailwayType = '';
        var railwayDiv;
        var trainListDiv;
        var table;
        for (var i = 0; i < trainList.length; i++) {
            var train = trainList[i];
            if (currRailwayType != train.type) {
                currRailwayType = train.type;
                railwayDiv = document.createElement('div');
                railwayDiv.classList.add('trainType');
                var railwayLink = document.createElement('a');
                railwayLink.id = currRailwayType;
                var img = document.createElement('img');
                img.src = 'images/' + currRailwayType + '.jpg';
                railwayLink.appendChild(img);
                railwayLink.addEventListener('click', function() {
                    var trainList = document.querySelectorAll('[id$=trainList]');
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
                document.querySelector('#trainSelector').appendChild(railwayDiv);

                trainListDiv = document.createElement('div');
                trainListDiv.id = currRailwayType + 'trainList';
                trainListDiv.classList.add('table-wrapper');
                trainListDiv.style.display = 'none';
                table = document.createElement('table');
                var thead = document.createElement('thead');
                var trHead = document.createElement('tr');
                var th1 = document.createElement('th1');
                trHead.appendChild(th1);
                thead.appendChild(trHead);
                table.appendChild(thead);
                trainListDiv.appendChild(table);
                document.querySelector('#trainSelector').appendChild(trainListDiv);
            }
            var linkControl = document.createElement('a');
            linkControl.setAttribute('id', train.trainId);
            linkControl.setAttribute('data-surveyedfrom', train.surveyedFrom);
            linkControl.addEventListener('click', function() {
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

/*			var linkDiv = document.createElement('div');
            linkDiv.classList.add('row');
            linkDiv.appendChild(linkControl);*/
            var tr = document.createElement('tr');
            var td = document.createElement('td');
            td.appendChild(linkControl);
            tr.appendChild(td);
            table.appendChild(tr);

            var searchCtrlDiv = document.createElement('div');
            trainListDiv.appendChild(searchCtrlDiv);
            // resuse proto
            proto.container = searchCtrlDiv;
            var searchCtrl = MYAPP.View.SearchTrain(proto);
            myModel.addObserver(COMM.event.modelReady, searchCtrl);
        }
    }

	that.onClick = function(newTrain) {
		this.notify(COMM.event.trainChanged, newTrain);
	}

	return that;
}
