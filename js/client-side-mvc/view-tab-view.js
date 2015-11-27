var MYAPP = MYAPP || {};
MYAPP.View = MYAPP.View || {};

MYAPP.View.TabView = function(proto) {
    var headers, contents, that;
    myModel = proto.model;
    status = "loading";
    that = {};
    that = COMM.Observer(that);

    that.trigger = function(eventName, params) {
        status = "ready";
        this.draw();
    }
    headers = new Array();
    contents = new Array();
    that.fillTabHeader = function(idx, content) {
        headers[idx] = content;
    }
    that.fillTabContent = function(idx, content) {
        contents[idx] = content;
    }
    that.draw = function() {
        var container, mainDiv, li, ul, width;
        if (status === 'loading') {
            return;
        }
        container = document.querySelector(proto.divId);
        if (!container) {
            console.log("TabView, cannot fin the div where to draw" + proto.divId);
            return;
        }
        mainDiv = document.createElement('div');
        container.appendChild(mainDiv);

        ul = document.createElement('ul');
        if (skel.getStateId() === "/global/xlarge") {
            //ul.id = "tabView";
            ul.setAttribute('class', 'tabViewList');
        } else {
            //ul.id = "tabViewMobile";
            ul.setAttribute('class', 'tabViewListMobile');
        }

        mainDiv.appendChild(ul);
        width = Math.floor(100 / headers.length);
        for(var i = 0; i < headers.length; i++) {
            li = document.createElement('li');
            li.setAttribute('class', 'tabView');
            li.setAttribute('style', 'width: ' + width + '%;');
            //li.appendChild(headers[i]);
            li.innerHTML =  headers[i];
            
            ul.appendChild(li);
        }
    }
    return that;
}
