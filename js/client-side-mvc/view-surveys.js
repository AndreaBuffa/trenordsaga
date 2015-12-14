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
        model.getSurveyGraphData(params, function(lineChartData, columnChartData) {
            status = "ready";
            that.draw(params, lineChartData, columnChartData);
        });
    };

    that.draw = function(params, lineChartData, columnChartData) {
        var columnChart, columnChartDataTable, columnChartOpt, div, div2,
        lineChart, lineChartDataTable, lineChartOptions;
        if (status === 'noBinded') {
            return;
        }
        lineChartDataTable = new google.visualization.DataTable(lineChartData);
        lineChartOptions = {
            title: '{{nls.trainNum}} ' + params.type + ' ' + params.trainId +
                   ' {{nls.left}} ' + params.leaveTime + ' {{nls.left_day}} ' +
                   params.selectedDate,
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
        lineChart = new google.visualization.LineChart(div);
        lineChart.draw(lineChartDataTable, lineChartOptions);

        columnChartOpt = {
            vAxis: {
                format: '',
                title: '{{ nls.delay_in_minutes }}'
            },
            title: '{{nls.trainNum}} ' + params.type + ' ' + params.trainId +
                   ' {{nls.left}} ' + params.leaveTime + ' {{nls.left_day}} ' +
                   params.selectedDate,
            legend: { position: 'top' },
            colors: ['#dc3912', '#33ac71']
        };
        div2 = document.getElementById(proto.divId2);
        if (!div2) {
            console.log('Surveys, cannot find div(' + proto.divId2 +')');
            return;
        }
        columnChart = new google.visualization.ColumnChart(div2);
        columnChartDataTable = new google.visualization.DataTable(columnChartData);
        columnChart.draw(columnChartDataTable, columnChartOpt);

        var table = new google.visualization.Table(document.getElementById('table_div'));
        table.draw(columnChartDataTable, {showRowNumber: true, width: '100%', height: '100%'});

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
            google.load("visualization", "1", { packages: ["corechart", "table"],
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
