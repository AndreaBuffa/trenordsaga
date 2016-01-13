var MYAPP = MYAPP || {};
MYAPP.View = MYAPP.View || {};

MYAPP.View.TypePicker = function(proto) {
/*  @todo check state
*/
    var anchor, myModel, status, that;
    anchor = proto.anchor;
    myModel = proto.model;
    status = "";
    that = COMM.Observer(proto);
    that = COMM.Notifier(that);

    that.trigger = function(eventName, params) {
        switch(eventName) {
            case COMM.event.modelReady:
                status = "ready";
                this.update();
            break;
            case COMM.event.docReady:
                status = "loading";
                this.draw();
            break;
        }
    };

    that.update = function() {
        myModel.getTrainList({}, function(trainList) {
            trainList = trainList || [];
            that.draw(trainList);
        });
    };

    that.draw = function(trainList) {
        var container = document.querySelector('#' + proto.divId), currRailwayType = '',
        label, railwayDiv, railwayLink, train;

        if (container) {
            while (container.hasChildNodes()) {
                container.removeChild(container.lastChild);
            }
        } else {
            console.log('Type-Picker, cannot find div container ' + proto.divId);
            return;
        }
        if (status === "loading") {
            container.innerHTML = "Loading....";
            return;
        }
        label = document.createElement('div');
        label.innerHTML = '<header class="major"><h2>{{ nls.choose_type }}</h2></header>';
        container.appendChild(label);

        for (var i = 0; i < trainList.length; i++) {
            train = trainList[i];
            if (currRailwayType != train.type) {
                currRailwayType = train.type;
                railwayDiv = document.createElement('div');
                railwayDiv.classList.add('trainType');
                railwayLink = document.createElement('a');
                railwayLink.id = currRailwayType;
                railwayLink.setAttribute('data-type', currRailwayType);
                railwayLink.innerHTML = COMM.getTrainIcon(currRailwayType);
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
