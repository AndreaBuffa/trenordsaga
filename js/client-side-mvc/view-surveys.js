{% autoescape off %}
var MYAPP = MYAPP || {};
MYAPP.View = MYAPP.View || {};

MYAPP.View.Surveys = function(proto) {
    var columnChartData, divIdx, displayMemento = [], model, params = {}, lineChartData,
    status, stateId, that;
    divIdx = {hd1: 0, chart1: 1, hd2: 2, chart2: 3, hd3: 4, chart3: 5,
        noSurvayMsg: 6};
    model = proto.model;
    stateId = {'hidden': 0, 'ready': 1, 'loading': 2};
    status = stateId.hidden;
    that = COMM.Observer(proto);
    that = COMM.DrawOnResize(that);

    that.trigger = function(eventName, _params) {
        switch(eventName) {
            case COMM.event.docReady:
            case COMM.event.modelReady:
            case COMM.event.libLoaded:
                that.update();
                that.draw();
            break;
            case COMM.event.trainChanged:
            case COMM.event.dateChanged:
                this.update(_params);
                if (status === stateId.hidden) {
                    status = stateId.loading;
                    that.draw();
                }
            break;
            case COMM.event.tabChanged:
                that.toggleDisplay(_params.visible);
            break;
        }
    };

    that = COMM.GChartsLibInit(that,
        function() {
            that.trigger(COMM.event.libLoaded);
    });

    that.update = function(_params) {
        if (_params) {
            params = _params;
        }

        model.getSurveyGraphData(params,
            function(_lineChartData, _columnChartData) {
                if (_lineChartData && _columnChartData) {
                    lineChartData = _lineChartData;
                    columnChartData = _columnChartData;
                }
                status = stateId.ready;
                that.draw();
            });
    };

    that.draw = function() {
        var columnChart, columnChartDataTable, columnChartOpt, dateFormatted,
        divIdList, divCtrlList = [], lineChart, lineChartDataTable,
        lineChartOptions, tableChart, trainDescr;
        if (status === stateId.hidden) {
            return;
        }
        divIdList = proto.divList;
        for (var i = 0; i < divIdList.length; i++) {
            divCtrlList.push(document.getElementById(divList[i]));
            if (!divCtrlList[divCtrlList.length - 1]) {
                console.log('Surveys, cannot find div(' +
                    divCtrlList[divCtrlList.length - 1] +')');
                return;
            }
        };
        if (status === stateId.loading) {
            divCtrlList[divIdx.chart1].setAttribute('style', 'display: block;');
            divCtrlList[divIdx.chart1].innerHTML = ".......loading..";
            return;
        }
        if (!that.getChartsLibReady()) {
            console.log('Surveys, chartsLibReady is false');
            return;
        }
//        if (!lineChartData.rows && !columnChartData.rows &&
//             lineChartData.rows.length === 0 && columnChartData.rows.length === 0) {
        if (!lineChartData.rows || lineChartData.rows.length === 0) {
            divCtrlList[divIdx.noSurvayMsg].setAttribute('style', 'display: block;');
            divCtrlList[divIdx.chart1].setAttribute('style', 'display: none;');
            trainDescr = model.getTrainDescr(params.trainId);
            divCtrlList[divIdx.noSurvayMsg].innerHTML = "<p>{{ nls.nosurvey }}</p>";
            if (trainDescr && trainDescr.notes) {
                divCtrlList[divIdx.noSurvayMsg].innerHTML += "<h2>&nbsp;</h2><i>" +
                    trainDescr.notes + "</i>";
            }
            return;
        }
        dateFormatted = COMM.toISOString(params.selectedDate);
        divCtrlList[divIdx.hd1].setAttribute('style', 'display: block;');
        lineChartDataTable = new google.visualization.DataTable(lineChartData);
        lineChartOptions = {
            title: '{{nls.trainNum}} ' + params.trainType + ' ' + params.trainId +
                   ' {{nls.left}} ' + params.leaveTime + ' {{nls.left_day}} ' +
                   dateFormatted,
            chartArea: {'width': '85%'},
            curveType: 'function',
            legend: {position: 'top',
                     textStyle: { bold: false}},
            tooltip: {trigger: 'selection'}
        };
        divCtrlList[divIdx.chart1].setAttribute('style', 'display: block;');
        lineChart = new google.visualization.LineChart(divCtrlList[divIdx.chart1]);
        lineChart.draw(lineChartDataTable, lineChartOptions);
        lineChart.setSelection([{
            row: Math.floor(lineChartDataTable.getNumberOfRows() / 2),
            column: 2}]);

        divCtrlList[divIdx.hd2].setAttribute('style', 'display: block;');
        columnChartOpt = {
            vAxis: {
                format: '',
                title: '{{ nls.delay_in_minutes }}'
            },
            chartArea: {'width': '90%'},
            title: '{{nls.trainNum}} ' + params.trainType + ' ' + params.trainId +
                   ' {{nls.left}} ' + params.leaveTime + ' {{nls.left_day}} ' +
                   dateFormatted,
            legend: {position: 'top'},
            colors: ['#dc3912', '#33ac71'],
            tooltip: {trigger: 'selection'}
        };
        divCtrlList[divIdx.chart2].setAttribute('style', 'display: block;');
        columnChart = new google.visualization.ColumnChart(divCtrlList[divIdx.chart2]);
        columnChartDataTable = new google.visualization.DataTable(columnChartData);
        columnChart.draw(columnChartDataTable, columnChartOpt);
        columnChart.setSelection([{
            row: Math.floor(columnChartDataTable.getNumberOfRows() / 2),
            column: 2}]);


        divCtrlList[divIdx.hd3].setAttribute('style', 'display: block;');
        divCtrlList[divIdx.chart3].setAttribute('style', 'display: block;');
        tableChart = new google.visualization.Table(divCtrlList[divIdx.chart3]);
        tableChart.draw(columnChartDataTable,
                        {showRowNumber: true, width: '100%', height: '100%'});
    }

    that.toggleDisplay = function(visible) {
        var tmp, divIdList = proto.divList, statusList;
        if (!visible) {
            displayMemento = [];
        }
        for (var i = 0; i < divIdList.length; i++) {
            tmp = document.getElementById(divIdList[i]);
            if (!tmp) {
                console.log('Surveys, cannot find div(' + divList[i] +')');
                return;
            }
            if (visible) {
                tmp.setAttribute('style', displayMemento[i]);
            } else {
                displayMemento.push(tmp.getAttribute('style'));
                tmp.setAttribute('style', 'display: none;');
            }
        };
        status = visible === true ? stateId.ready: stateId.hidden;
    }

    return that.init();
}
{% endautoescape %}
