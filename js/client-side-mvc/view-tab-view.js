var MYAPP = MYAPP || {};
MYAPP.View = MYAPP.View || {};

MYAPP.View.TabView = function(proto) {
    var headers, contents, liCtrlArray, that;
    liCtrlArray = new Array();
    status = "loading";
    that = {};
    that = COMM.Observer(that);

    that.trigger = function(eventName, params) {
        status = "ready";
        this.draw();
        this.setTabFocus(0);
    }

    that.setTabFocus = function(idx) {
        var contentCtrl, event;
        if (idx >= 0 && idx < liCtrlArray.length) {
            if (liCtrlArray[idx]) {
                event = document.createEvent('Event');
                event.initEvent('click', true, true);
                liCtrlArray[idx].dispatchEvent(event);
            } else {
                console.log('TabView, no li ctrl for index (' + idx + ')');
            }
        } else {
            if (idx === -1) {
                for(var i = 0; i < liCtrlArray.length; i++) {
                    contentCtrl = document.querySelector('#' + liCtrlArray[i].dataset.contentid);
                    if (contentCtrl)
                        contentCtrl.style.display = 'none';
                    liCtrlArray[i].innerHTML = headers[i];
                }
            } else {
                console.log('TabView, cannot set focus for index (' + idx + ')');
            }
        }
    }

    headers = new Array();
    contents = new Array();
    that.fillTabHeader = function(idx, content) {
        headers[idx] = content;
    }

    that.fillTabContent = function(idx, divId) {
        contents[idx] = divId;
    }

    that.draw = function() {
        var container, div, mainDiv, li, ul, width;
        if (status === 'loading') {
            return;
        }
        container = document.querySelector(proto.divId);
        if (!container) {
            console.log("TabView, cannot fin the div where to draw" + proto.divId);
            return;
        }
        //mainDiv = document.createElement('div');
        //container.appendChild(mainDiv);

        ul = container.getElementsByTagName('ul')[0];
        /*
        if (skel.getStateId() === "/global/xlarge") {
            //ul.id = "tabView";
            ul.setAttribute('class', 'tabViewList');
        } else {
            //ul.id = "tabViewMobile";
            ul.setAttribute('class', 'tabViewListMobile');
        } */

        //mainDiv.appendChild(ul);
        width = Math.floor(100 / headers.length);
        for(var i = 0; i < headers.length; i++) {
            li = document.createElement('li');
            liCtrlArray.push(li);
            //li.setAttribute('class', 'tabView');
            //li.setAttribute('style', 'width: ' + width + '%;');
            //li.setAttribute('style', 'width: ' + (i === 0 ? '120px;': width + '%;'));
            //li.appendChild(headers[i]);
            if (i < contents.length) {
                li.setAttribute('data-contentid', contents[i]);
            }
            li.addEventListener('click', function() {
                var contentCtrl, j, liCtrl;
                for(var i = 0,j = 0; i < this.parentElement.childElementCount; i++) {
                    liCtrl = this.parentElement.children[i];
                    if (!liCtrl.dataset.contentid) {
                        continue;
                    }
                    if (liCtrl === this) {
                        liCtrl.classList.add('active');
                        contentCtrl = document.querySelector('#' + liCtrl.dataset.contentid);
                        if (contentCtrl)
                            contentCtrl.style.display = 'block';
                    } else {
                        liCtrl.classList.remove('active');
                        contentCtrl = document.querySelector('#' + liCtrl.dataset.contentid);
                        if (contentCtrl)
                            contentCtrl.style.display = 'none';
                    }
                    liCtrl.innerHTML = headers[j];
                    j++;
                }
            });
            div = document.createElement('div');
            div.innerHTML = headers[i];
            li.appendChild(div);
            ul.appendChild(li);
        }
    }
    return that;
}
