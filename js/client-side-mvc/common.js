"use strict";
var COMM = COMM || {};

COMM.lineIcon = '<svg class="svgIcon" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" version="1.0" x="0px" y="0px" viewBox="0 0 24 24" enable-background="new 0 0 24 24" xml:space="preserve"><polygon points="15.997,6.814 13.534,4.467 13.155,4.09 12.814,4.467 10.428,6.814 11.186,7.611 12.662,6.096 12.662,8.859   10.579,10.979 9.064,9.465 9.064,4.883 8.003,4.883 8.003,9.729 8.003,9.92 8.155,10.107 9.784,11.734 8.155,13.361 8.003,13.514   8.003,13.742 8.003,19.154 9.064,19.154 9.064,13.969 10.579,12.453 12.662,14.611 12.662,17.906 11.186,16.43 10.428,17.148   12.814,19.533 13.155,19.91 13.534,19.533 15.997,17.225 15.238,16.43 13.724,17.869 13.724,14.385 13.724,14.158 13.571,14.008   11.299,11.734 13.571,9.465 13.724,9.314 13.724,9.086 13.724,6.135 15.238,7.57 15.997,6.814 "></polygon></svg>';
COMM.trainIcon = '<svg class="svgIcon" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" version="1.1" x="0px" y="0px" viewBox="0 0 100 125" enable-background="new 0 0 100 100" xml:space="preserve"><g display="none"><path display="inline" d="M94.936,32.25l-22.879,8.623v-7.869c0-4.341-3.532-7.873-7.871-7.873H12.937   c-4.339,0-7.872,3.532-7.872,7.873v33.992c0,4.342,3.533,7.873,7.872,7.873h51.249c4.339,0,7.871-3.531,7.871-7.873v-7.629   l22.879,8.357V32.25z M68.908,66.996c0,2.605-2.121,4.723-4.723,4.723H12.937c-2.604,0-4.723-2.117-4.723-4.723V33.004   c0-2.605,2.118-4.724,4.723-4.724h51.249c2.602,0,4.723,2.118,4.723,4.724V66.996z M91.787,63.223L72.22,56.076V44.174   l19.567-7.372V63.223z"/></g><g><path d="M76.651,87.363l-6.809-5.889c3.59-0.83,6.272-4.032,6.272-7.873V22.586c0-4.472-3.627-8.098-8.098-8.098h-4.033v-3.948   c0-1.789-1.45-3.239-3.238-3.239h-1.722c-1.788,0-3.239,1.45-3.239,3.239v3.948H44.044v-3.948c0-1.789-1.45-3.239-3.239-3.239   h-1.721c-1.789,0-3.239,1.45-3.239,3.239v3.948h-4.065c-4.472,0-8.098,3.625-8.098,8.098v51.015c0,3.897,2.753,7.145,6.421,7.919   l-6.756,5.843c-1.268,1.098-1.407,3.015-0.31,4.284c1.098,1.27,3.014,1.407,4.283,0.309L39.18,81.698h21.642l11.855,10.258   c1.269,1.099,3.186,0.961,4.283-0.309S77.922,88.461,76.651,87.363z M35.76,72.05c-2.907,0-5.264-2.356-5.264-5.263   c0-2.909,2.356-5.266,5.264-5.266c2.908,0,5.264,2.356,5.264,5.266C41.024,69.693,38.668,72.05,35.76,72.05z M64.136,72.05   c-2.906,0-5.263-2.356-5.263-5.263c0-2.909,2.356-5.266,5.263-5.266c2.907,0,5.264,2.356,5.264,5.266   C69.399,69.693,67.043,72.05,64.136,72.05z M69.435,43.574c0,1.787-1.452,3.239-3.239,3.239h-32.39   c-1.79,0-3.239-1.452-3.239-3.239V30.751c0-1.789,1.449-3.239,3.239-3.239h32.39c1.787,0,3.239,1.45,3.239,3.239V43.574z"/></g></svg>';
COMM.calendarIcon = '<?xml version="1.0" encoding="utf-8"?><!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd"><svg class="svgIcon" version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px" viewBox="0 0 88 125" enable-background="new 0 0 88 100" xml:space="preserve"><path d="M0,32v59.906C0,96.377,3.582,100,8,100h72c4.418,0,8-3.623,8-8.094V32H0z M22,94H6V78h16V94z M22,74H6V58h16V74z M22,54H6	V38h16V54z M42,94H26V78h16V94z M42,74H26V58h16V74z M42,54H26V38h16V54z M62,94H46V78h16V94z M62,74H46V58h16V74z M62,54H46V38h16	V54z M82,94H66V78h16V94z M82,74H66V58h16V74z M82,54H66V38h16V54z"/><path d="M80,12H67V3c0-1.657-1.344-3-3-3c-1.657,0-3,1.343-3,3v9H27V3c0-1.657-1.344-3-3-3c-1.657,0-3,1.343-3,3v9H8 c-4.418,0-8,3.623-8,8.093V27v0v1h88v-1v0v-6.907C88,15.623,84.418,12,80,12z M24,26c-3.313,0-6-2.687-6-6	c0-2.219,1.209-4.152,3-5.19V20c0,1.657,1.343,3,3,3c1.656,0,3-1.343,3-3v-5.191c1.792,1.038,3,2.972,3,5.191	C30,23.313,27.314,26,24,26z M64,26c-3.313,0-6-2.687-6-6c0-2.219,1.209-4.152,3-5.19V20c0,1.657,1.343,3,3,3c1.656,0,3-1.343,3-3	v-5.191c1.792,1.038,3,2.972,3,5.191C70,23.313,67.314,26,64,26z"/></svg>';

COMM.frecceIcon = '<?xml version="1.0" encoding="UTF-8" standalone="no"?> <!-- Created with Inkscape (http://www.inkscape.org/) --> <svg class="typeIcon" xmlns:dc="http://purl.org/dc/elements/1.1/"xmlns:cc="http://creativecommons.org/ns#"xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"xmlns:svg="http://www.w3.org/2000/svg"xmlns="http://www.w3.org/2000/svg"xmlns:sodipodi="http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd"xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape"width="50"height="50"viewBox="0 0 24.999999 24.999999"id="svg2"version="1.1"inkscape:version="0.91 r13725"sodipodi:docname="Frecce.svg"> <defs id="defs4" /> <sodipodi:namedview id="base"pagecolor="#ffffff"bordercolor="#666666"borderopacity="1.0"inkscape:pageopacity="0.0"inkscape:pageshadow="2"inkscape:zoom="17.196837"inkscape:cx="17.861037"inkscape:cy="13.080605"inkscape:document-units="px"inkscape:current-layer="layer1"showgrid="false"inkscape:window-width="1213"inkscape:window-height="673"inkscape:window-x="63"inkscape:window-y="6"inkscape:window-maximized="0"units="px" /> <metadata id="metadata7"> <rdf:RDF> <cc:Work rdf:about=""> <dc:format>image/svg+xml</dc:format> <dc:type rdf:resource="http://purl.org/dc/dcmitype/StillImage" /> <dc:title></dc:title> </cc:Work> </rdf:RDF> </metadata> <g inkscape:label="Layer 1"inkscape:groupmode="layer"id="layer1"transform="translate(0,-1027.3622)"> <rect style="fill:#cf142d;fill-rule:evenodd;stroke:#cf142d;stroke-width:0.49999994;stroke-linecap:butt;stroke-linejoin:miter;stroke-opacity:1;fill-opacity:1;stroke-miterlimit:4;stroke-dasharray:none"id="rect5439"width="24.44305"height="24.44305"x="0.2784732"y="1027.6406"ry="2.265105" /> <text xml:space="preserve"style="font-style:normal;font-variant:normal;font-weight:900;font-stretch:normal;font-size:7.66808081px;line-height:100%;font-family:\'Arial Black\';-inkscape-font-specification:\'Arial Black, Heavy\';text-align:start;letter-spacing:0px;word-spacing:0px;writing-mode:lr-tb;text-anchor:start;fill:#ffffff;fill-opacity:1;stroke:none;stroke-width:1px;stroke-linecap:butt;stroke-linejoin:miter;stroke-opacity:1"x="0.9296878"y="840.06323"id="text5445"sodipodi:linespacing="100%"transform="scale(0.80562007,1.2412799)"><tspan sodipodi:role="line"id="tspan5447"x="0.9296878"y="840.06323"style="font-style:normal;font-variant:normal;font-weight:900;font-stretch:normal;font-size:7.66808081px;line-height:100%;font-family:\'Arial Black\';-inkscape-font-specification:\'Arial Black, Heavy\';text-align:start;writing-mode:lr-tb;text-anchor:start">Frecce</tspan></text> </g> </svg>';

COMM.colorList = {'EC': '#666666', 'REG': '#0660A8', 'S1': '#ff1822',
'S2': '#029779', 'S3': '#029677', 'S4': '#83BB24', 'S5': '#FE7D20',
'S6': '#F0D40D', 'S7': '#CD0294', 'S8': '#FF9EC9', 'S9': '#A6023B',
'S11': '#919DFF', 'S13': '#663c01', 'S14': '#CDCC67' };

COMM.textList = {'S1': '&nbsp;S1', 'S2': '&nbsp;S2', 'S3': '&nbsp;S3',
'S4': '&nbsp;S4', 'S5': '&nbsp;S5', 'S6': '&nbsp;S6', 'S8': '&nbsp;S8',
'S9': '&nbsp;S9', 'S11': 'S11', 'S13': 'S13', 'REG': '&nbsp;RE', 'EC': '&nbsp;EC'};


COMM.isMobile = function() {
    switch (skel.getStateId()) {
        case "/global/xlarge":
        case "/global/xlarge/large":
            return false;
        break;
    }
    return true;
}

COMM.isArray = function(myArray) {
    if (myArray) {
        return myArray.constructor.toString().indexOf("Array") > -1;
    }
    return false;
};

COMM.Observer = function(that) {
    that.trigger = function(eventName, params) {
        console.log("Implement me...");
    };
    return that;
};

COMM.Notifier = function (that) {
    that.observerList = {};
    that.addObserver = function(eventName, observer) {
        //check observer type
        if (COMM.isArray(that.observerList[eventName])) {
            that.observerList[eventName].push(observer);
        } else {
            that.observerList[eventName] = [observer];
        }
    };
    that.notify = function(eventName, params) {
        if (COMM.isArray(that.observerList[eventName])) {
            for (var i = 0; i < that.observerList[eventName].length; i++) {
                that.observerList[eventName][i].trigger(eventName, params);
            }
        } else {
            console.log("No observer registered to this event:" + eventName);
        }
    };
    return that;
};

COMM.event = {
    modelReady: "modelReady",
    typeChanged: "typeChanged",
    trainChanged: "trainChanged",
    dateChanged: "dateChanged",
    docReady: "docReady",
    libLoaded: "libLoaded",
    tabChanged: "tabChanged",
    scrollUp: "scrollUp"
};

COMM.GChartsLibInit = function(that, _callback) {
    var scriptIdLib = 'gjslibs', libReady = false;
    that.init = function() {
        var head, script = document.createElement("script");
        script.setAttribute('id', scriptIdLib);
        script.setAttribute('async', 'async');
        script.setAttribute('src', 'https://www.google.com/jsapi');
        script.onload = function() {
            google.load("visualization", "1", {packages: ["corechart", "table"],
                                               callback:
                                                    function() {
                                                       libReady = true;
                                                        _callback();
                                                    }
                                               });
        }
        if (!document.getElementById(scriptIdLib)) {
            head = document.getElementsByTagName('head')[0];
            head.appendChild(script);
        }
        return that;
    }
    that.getChartsLibReady = function() {
        return libReady;
    }
    return that.init();
}

COMM.DrawOnResize = function(that) {
    $(window).resize(function(){
        that.draw();
    });
    return that;
}

COMM.getTrainIcon = function(trainType) {
    if (trainType === 'Frecciarossa') {
        return COMM.frecceIcon;
    } else {
        return '<?xml version="1.0" encoding="UTF-8" standalone="no"?> <svg class="typeIcon" xmlns:dc="http://purl.org/dc/elements/1.1/"xmlns:cc="http://creativecommons.org/ns#"xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"xmlns:svg="http://www.w3.org/2000/svg"xmlns="http://www.w3.org/2000/svg"xmlns:sodipodi="http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd"xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape"width="50"height="50"viewBox="0 0 24.999999 24.999999"id="svg2"version="1.1"inkscape:version="0.91 r13725"> <defs id="defs4" /> <sodipodi:namedview id="base"pagecolor="#ffffff"bordercolor="#666666"borderopacity="1.0"inkscape:pageopacity="0.0"inkscape:pageshadow="2"inkscape:zoom="12.16"inkscape:cx="21.384566"inkscape:cy="12.776081"inkscape:document-units="px"inkscape:current-layer="layer1"showgrid="false"inkscape:window-width="1213"inkscape:window-height="673"inkscape:window-x="69"inkscape:window-y="28"inkscape:window-maximized="0"units="px" /> <metadata id="metadata7"> <rdf:RDF> <cc:Work rdf:about=""> <dc:format>image/svg+xml</dc:format> <dc:type rdf:resource="http://purl.org/dc/dcmitype/StillImage" /> <dc:title></dc:title> </cc:Work> </rdf:RDF> </metadata> <g inkscape:label="Layer 1"inkscape:groupmode="layer"id="layer1"transform="translate(0,-1027.3622)"> <rect style="fill:' + 
            COMM.colorList[trainType] + ';fill-rule:evenodd;stroke:' + COMM.colorList[trainType] + ';stroke-width:0.49999994;stroke-linecap:butt;stroke-linejoin:miter;stroke-opacity:1;fill-opacity:1;stroke-miterlimit:4;stroke-dasharray:none"id="rect5439"width="24.44305"height="24.44305"x="0.2784732"y="1027.6406"ry="2.265105" /> <text xml:space="preserve"style="font-style:normal;font-variant:normal;font-weight:900;font-stretch:normal;font-size:9.99999905px;line-height:100%;font-family:\'Arial Black\';-inkscape-font-specification:\'Arial Black, Heavy\';text-align:start;letter-spacing:0px;word-spacing:0px;writing-mode:lr-tb;text-anchor:start;fill:#ffffff;fill-opacity:1;stroke:none;stroke-width:1px;stroke-linecap:butt;stroke-linejoin:miter;stroke-opacity:1"x="2.3775535"y="1030.7755"id="text5445"sodipodi:linespacing="100%"transform="scale(0.98840972,1.0117262)"><tspan sodipodi:role="line"id="tspan5447"x="2.3775535"y="1030.7755">' +
            COMM.textList[trainType] + '</tspan></text> </g> </svg>';
    }
}

COMM.toISOString = function(currentDate) {
    var match = [];
    match = currentDate.match(/^(\d{4,})\-(\d+)\-(\d+)/);
    if (match == null || match.length < 3) {
        console.log("DateFormat, Invalid dateformat");
    }
    if ('{{nls.flag}}' === 'it-IT') {
        match.shift();
        return match.reverse().join("-");
    } else {
        return match[0];
    }
}

COMM.getYesterdayDate = function() {
    var yesterday, today = new Date();
    yesterday = new Date(today.getFullYear(), today.getMonth(),
                         today.getDate() - 1);

    return yesterday.toISOString().substring(0,10);
}

COMM.MenuLiBuilder = function(that) {
    if (!that) {
        console.log("that MenuLiBuilder is NULL");
        return;
    }
    that.getTypeLi = function(trainType) {
        return COMM.lineIcon + COMM.getTrainIcon(trainType);
    };
    that.getTrainNumLi = function(trainNum) {
        return COMM.trainIcon + trainNum;
    };
    that.getCalendarLi = function(currDate) {
        return COMM.calendarIcon + currDate;
    };
    return that;
}

COMM.DocReadyDispatcher = function(proto) {
    var that = {};
    that = COMM.Notifier(that);
    that.init = function() {
        $(document).ready(function() {
            that.notify(COMM.event.docReady);
        });
        return that;
    }
    return that.init();
}

COMM.ScrollUpDispatcher = function(that) {
    if (!that) {
        console.log("that ScrollUpDispatcher is NULL");
        return;
    }
    that = COMM.Notifier(that);
    var lastScrollTop = 0;
    that.init = function() {
        $(window).scroll(function(event){
           var st = $(this).scrollTop();
           if (st > lastScrollTop){
               // downscroll code
           } else {
                that.notify(COMM.event.scrollUp);
           }
           lastScrollTop = st;
        });
        return that;
    }   
    return that.init();
}

COMM.writeTable = function(labels, dataset, attributes) {
    var dataTd, dataTr;
    var table = document.createElement('table');
    var tbody = document.createElement('tbody');
    var th;
    var thead = document.createElement('thead');
    var trHead = document.createElement('tr');

    for (var i = 0; i < labels.length; i++) {
        th = document.createElement('th');
        th.innerHTML = labels[i];
        trHead.appendChild(th);
    }
    thead.appendChild(trHead);
    table.appendChild(thead);
    table.appendChild(tbody);
    for (var i = 0; i < dataset.length; i++) {
        dataTr = document.createElement('tr');
        for (var j = 0; j < attributes.length; j++) {
            dataTd = document.createElement('td');
            dataTd.innerHTML += dataset[i][attributes[j]];
            dataTr.appendChild(dataTd);
        }
        tbody.appendChild(dataTr);
    }
    return table;
};
