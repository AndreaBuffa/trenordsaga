var MYAPP = MYAPP || {};
MYAPP.View = MYAPP.View || {};

MYAPP.View.Surveys = function(proto) {
    var chartsLibReady = false, model, status, that;
    model = proto.model;
    status = "noBinded";
    that = COMM.Observer(proto);

    that.trigger = function(eventName, params) {
        switch(eventName) {
            case COMM.event.modelReady:
                if (chartsLibReady)
                    this.draw();
            break;
            case COMM.event.dateChanged:
                status = "loading";
                this.update(params);
                return
            break;
        }
    };

    that.update = function(params) {
        model.getSurveyGraphData(params, function(columnChartData) {
            status = "ready";
            that.draw(columnChartData);
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

    that.toggle = function(visible) {
        var div = document.getElementById(proto.divId);
        if (!div) {
            console.log('Surveys, cannot find div(' + proto.divId +')');
            return;
        }
        if (visible)
            div.style.display = 'table';
        else
            div.style.display = 'hidden';
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
