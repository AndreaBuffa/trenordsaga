var MYAPP = MYAPP || {};
MYAPP.View = MYAPP.View || {};

MYAPP.View.TrainSelector = function(proto) {
/*  @todo check state
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
/*          trainList.sort(function(a, b) {
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
        currRailwayType = '', from = '', railwayDiv, railwayLink, table, td, th1, thead, to = '', tr, trHead, train, trainListDiv;

        if (container) {
            while (container.hasChildNodes()) {
                container.removeChild(container.lastChild);
            }
        } else {
            container = document.createElement('div');
            container.setAttribute('id', 'trainSelector');
            document.querySelector('#type').appendChild(container);
        }
        if (status === "loading") {
            container.innerHTML = "Loading....";
            return;
        }

        for (var i = 0; i < trainList.length; i++) {
            train = trainList[i];
            if (currRailwayType != train.type) {
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
            }
        }
    };

    that.onClick = function(newTrain) {
        this.notify(COMM.event.trainChanged, newTrain);
    };

    return that;
}
