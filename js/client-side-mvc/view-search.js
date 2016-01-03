var MYAPP = MYAPP || {};
MYAPP.View = MYAPP.View || {};

MYAPP.View.Search = function(proto) {
    var myModel, status, that;
    myModel = proto.model;
    status = "";
    that = COMM.Observer(proto);

    that.trigger = function(eventName, params) {
        switch(eventName) {
            case COMM.event.modelReady:
                status = "ready";
                this.update();
            break;
            case COMM.event.docReady:
                status = "loading";
            break;
            case COMM.event.scrollUp:
            	if (status === "ready") {
            		status = "visible";
            		that.draw();
            	}
            break;
        }
    };

    that.update = function() {
    };

    that.draw = function(trainList) {
    	var container = document.querySelector('#' + proto.divId), link;
    	if (!container) {
    		console.log('Search, cannot find div (' + proto.divId + ')');
    		return;
    	}
    	if (status === "") {
    		return;
    	}
    	if (status === "loading") {
    		container.innerHTML = "loading...";
    		return;
    	}
    	if (status === "visible") {
            link = document.createElement('a');
            link.setAttribute('href', '/search');
            link.innerHTML = "ricerca avanzata";
            container.appendChild(link);
            $('#' + proto.divId).slideDown( "slow" );
    		return;
    	}
    }
    return that;
}
