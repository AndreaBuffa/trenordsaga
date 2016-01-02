var MYAPP = MYAPP || {};
MYAPP.View = MYAPP.View || {};

MYAPP.View.Surveys = function(proto) {
    var chartsLibReady = false, columnChartData, model, params, lineChartData,
    status, that;
    model = proto.model;
    status = "noBinded";
    that = COMM.Observer(proto);

    that.trigger = function(eventName, param) {
        switch(eventName) {
            case COMM.event.modelReady:
                if (chartsLibReady)
                    this.draw();
            break;
            case COMM.event.dateChanged:
                status = "loading";
                this.update(param);
            break;
            case COMM.event.tabChanged:
                if (param.visible === false) {
                    that.hide();
                }
            break;
        }
    };

    that.update = function(param) {
        model.getSurveyGraphData(param, function(lineChartData, columnChartData) {
            status = "ready";
            that.draw(param, lineChartData, columnChartData);
        });
    };

    that.draw = function(_params, _lineChartData, _columnChartData) {
        var columnChart, columnChartDataTable, columnChartOpt, div, div2, div3,
        lineChart, lineChartDataTable, lineChartOptions, tableChart;
        if (_params && _lineChartData && _columnChartData) {
            params = _params;
            lineChartData = _lineChartData;
            columnChartData =  _columnChartData
        }
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
                },
            tooltip: { trigger: 'selection' }
        };
        div = document.getElementById(proto.divId);
        if (!div) {
            console.log('Surveys, cannot find div(' + proto.divId +')');
            return;
        }
        div.setAttribute('style', 'display: block;');
        lineChart = new google.visualization.LineChart(div);
        lineChart.draw(lineChartDataTable, lineChartOptions);
        lineChart.setSelection([{row: 3, column: 2}]);

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
        div2.setAttribute('style', 'display: block;');
        columnChart = new google.visualization.ColumnChart(div2);
        columnChartDataTable = new google.visualization.DataTable(columnChartData);
        columnChart.draw(columnChartDataTable, columnChartOpt);

        div3 = document.getElementById(proto.divId3);
        if (!div3) {
            console.log('Surveys, cannot find div(' + proto.divId3 +')');
            return;
        }
        div3.setAttribute('style', 'display: block;');

        tableChart = new google.visualization.Table(div3);
        tableChart.draw(columnChartDataTable,
                        { showRowNumber: true, width: '100%', height: '100%'});
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

    that.hide = function() {
        var divList = [], tmp;
        divList.push(proto.divId);
        divList.push(proto.divId2);
        divList.push(proto.divId3);
        for (var i = 0; i < divList.length; i++) {
            tmp = document.getElementById(divList[i]);
            if (!tmp) {
                console.log('Surveys, cannot find div(' + divList[i] +')');
                return;
            }
            tmp.setAttribute('style', 'display: none;');
        };
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
        $(window).resize(function(){
            that.draw();
        });
        return that;
    }

    return that.init();
}
