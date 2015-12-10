var MYAPP = MYAPP || {};
MYAPP.View = MYAPP.View || {};

MYAPP.View.Surveys = function(proto) {
    var chartsLibReady = false, modelReady = false, model, status, that;
    model = proto.model;
    status = "noBinded";
    that = COMM.Observer(proto);

    that.trigger = function(eventName, params) {
        switch(eventName) {
            case COMM.event.modelReady:
                modelReady = true;
            break;
            case COMM.event.dateChanged:
                status = "loading";
            break;
        }
        if (chartsLibReady && modelReady) {
            this.update();
        }
    };

    that.update = function() {
        that.draw({cols: [{label: "stop", pattern: "", type: "string"},
				     {label: "Previsto", pattern: "", type: "timeofday"},
				     {label: "Effettivo", pattern: "", type: "timeofday"},
				     {type: "boolean", p: {"role": "certainty"}}
				    ],
			      rows: [{c: [{v: "Albairate Vermezzo", f: null}, {v: [8,8,0,0], f:null}, {v: [8,12,0,0], f: "08:12 (4 minuti)"}, {v: true, f: "test"}]},{c: [{v: "Gaggiano", f: null}, {v: [8,13,0,0], f:null}, {v: [8,17,0,0], f: "08:17 (4 minuti)"}, {v: true, f: "test"}]},{c: [{v: "Trezzano S.N.", f: null}, {v: [8,17,0,0], f:null}, {v: [8,21,0,0], f: "08:21 (4 minuti)"}, {v: false, f: "test"}]},{c: [{v: "Cesano Boscone", f: null}, {v: [8,21,0,0], f:null}, {v: [8,25,0,0], f: "08:25 (4 minuti)"}, {v: false, f: "test"}]},{c: [{v: "Corsico", f: null}, {v: [8,24,0,0], f:null}, {v: [8,28,0,0], f: "08:28 (4 minuti)"}, {v: false, f: "test"}]},{c: [{v: "Milano S. Cristoforo", f: null}, {v: [8,30,0,0], f:null}, {v: [8,28,0,0], f: "08:28, in anticipo"}, {v: true, f: "test"}]},{c: [{v: "Milano Romolo", f: null}, {v: [8,35,0,0], f:null}, {v: [8,33,0,0], f: "08:33, in anticipo"}, {v: true, f: "test"}]},{c: [{v: "Milano Porta Romana", f: null}, {v: [8,41,0,0], f:null}, {v: [8,39,0,0], f: "08:39, in anticipo"}, {v: false, f: "test"}]},{c: [{v: "Milano Lambrate", f: null}, {v: [8,55,0,0], f:null}, {v: [8,53,0,0], f: "08:53, in anticipo"}, {v: true, f: "test"}]},{c: [{v: "Milano Greco Pirelli", f: null}, {v: [9,2,0,0], f:null}, {v: [9,1,0,0], f: "09:01, in anticipo"}, {v: true, f: "test"}]},{c: [{v: "Sesto S. Giovanni", f: null}, {v: [9,6,0,0], f:null}, {v: [9,7,0,0], f: "09:07 (1 minuto)"}, {v: true, f: "test"}]},{c: [{v: "Monza", f: null}, {v: [9,11,0,0], f:null}, {v: [9,12,0,0], f: "09:12 (1 minuto)"}, {v: true, f: "test"}]},{c: [{v: "Lissone-Muggio`", f: null}, {v: [9,16,0,0], f:null}, {v: [9,17,0,0], f: "09:17 (1 minuto)"}, {v: true, f: "test"}]},{c: [{v: "Desio", f: null}, {v: [9,20,0,0], f:null}, {v: [9,21,0,0], f: "09:21 (1 minuto)"}, {v: true, f: "test"}]},{c: [{v: "Seregno", f: null}, {v: [9,26,0,0], f:null}, {v: [9,28,0,0], f: "09:28 (2 minuti)"}, {v: true, f: "test"}]},{c: [{v: "Barruccana", f: null}, {v: [9,35,0,0], f:null}, {v: [9,38,0,0], f: "09:38 (3 minuti)"}, {v: true, f: "test"}]},{c: [{v: "Cesano Maderno", f: null}, {v: [9,37,0,0], f:null}, {v: [9,40,0,0], f: "09:40 (3 minuti)"}, {v: true, f: "test"}]},{c: [{v: "Groane", f: null}, {v: [9,44,0,0], f:null}, {v: [9,47,0,0], f: "09:47 (3 minuti)"}, {v: true, f: "test"}]},{c: [{v: "Cerlano Laghetto", f: null}, {v: [9,46,0,0], f:null}, {v: [9,49,0,0], f: "09:49 (3 minuti)"}, {v: true, f: "test"}]},{c: [{v: "Saronno Sud", f: null}, {v: [9,50,0,0], f:null}, {v: [9,53,0,0], f: "09:53 (3 minuti)"}, {v: true, f: "test"}]},{c: [{v: "Saronno", f: null}, {v: [9,54,0,0], f:null}, {v: [9,57,0,0], f: "09:57 (3 minuti)"}, {v: true, f: "test"}]} ]
			     });
    };

    that.draw = function(columnChartData) {
        var columnchart, columnChartOptions, div;
        if (status === 'noBinded') {
            return;
        }
        columnChartData = new google.visualization.DataTable(columnChartData);
        columnChartOptions = {
            title: '{{nls.trainNum}} {{trainType}} {{trainNum}} {{nls.left}} {{leaveTime}} {{nls.left_day}} {{date}}',
            curveType: 'function',
            legend: { position: 'top',
                  textStyle: { bold: false}
                }
        };
        div = document.getElementById(proto.divId);
        if (!div) {
            console.log('Surveys, cannot find div(' + proto.divId +')');
            return;
        }
        columnchart = new google.visualization.LineChart(div);
        columnchart.draw(columnChartData, columnChartOptions);
    }

    that.init = function() {
        var head, script = document.createElement("script");
        script.setAttribute('async', 'async');
        script.setAttribute('src', 'https://www.google.com/jsapi');
        script.onload = function() {
            google.load("visualization", "1", { packages: ["corechart"],
                                                callback: function() {
                                                        chartsLibReady = true;
                                                    }
                                               });
        }
        head = document.getElementsByTagName('head')[0];
        head.appendChild(script);
        return that;
    }

    return that.init();
}
