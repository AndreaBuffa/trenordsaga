var MYAPP = MYAPP || {};
MYAPP.View = MYAPP.View || {};

MYAPP.View.SearchTrain = function(proto) {
    var status = "disabled";
    var container = proto.container;
    var that = COMM.Observer(proto)

    if (!proto.model) {
        console.log("SearchTrain, I need a model");
    }

    if (!proto.container) {
        console.log("SearchTrain, I need a div container");
    }

    that.trigger = function(eventName, params) {
        if (spec.eventName === COMM.event.modelReady) {
            status = "collapsed";
            this.update();
        } else {
            log.console("Not listening to " + eventName);
        }
    }

    that.update = function () {
        this.draw();
    }

    that.draw = function () {
        container.innerHTML = "Test....";
    }
	that.draw();
    return that;
}
