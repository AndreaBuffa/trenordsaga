var MYAPP = MYAPP || {};
MYAPP.View = MYAPP.View || {};

MYAPP.View.TypePicker = function(proto) {
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
        myModel.getTrainList({}, function(trainList) {
            trainList = trainList || [];
          trainList.sort(function(a, b) {
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
            });
            status = "ready";
            that.draw(trainList);
        });
    };

    that.draw = function(trainList) {
        var container = document.querySelector('#' + proto.divId), img,
        currRailwayType = '', railwayDiv, railwayLink, train, trainListDiv;

        if (container) {
            while (container.hasChildNodes()) {
                container.removeChild(container.lastChild);
            }
        } else {
            container = document.createElement('div');
            container.setAttribute('id', proto.divId);
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
                railwayLink.setAttribute('data-type', currRailwayType);
                img = document.createElement('img');
                img.src = 'images/' + currRailwayType + '.jpg';
                railwayLink.appendChild(img);
                railwayLink.addEventListener('click', function() {
                    that.notify(COMM.event.typeChanged,
                                {'trainType': this.dataset.type});
                });
                railwayDiv.appendChild(railwayLink);
                container.appendChild(railwayDiv);
            }
        }
    };
    return that;
}
