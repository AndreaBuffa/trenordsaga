{% autoescape off %}
var MYAPP = MYAPP || {};
MYAPP.View = MYAPP.View || {};

MYAPP.View.Surveys = function(proto) {
    var columnChartData, divIdx, model, params, lineChartData, status, that;
    divIdx = {hd1: 0, chart1: 1, hd2: 2, chart2: 3, hd3: 4, chart3: 5,
        noSurvayMsg: 6};
    model = proto.model;
    status = '';
    that = COMM.Observer(proto);
    that = COMM.GChartsLibInit(that);
    that = COMM.DrawOnResize(that);

    that.trigger = function(eventName, param) {
        switch(eventName) {
            case COMM.event.dateChanged:
                this.update(param);
                status = 'loading';
                that.draw();
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
            status = 'ready';
            that.draw(param, lineChartData, columnChartData);
        });
    };

    that.draw = function(_params, _lineChartData, _columnChartData) {
        var columnChart, columnChartDataTable, columnChartOpt, divIdList,
        divCtrlList = [],lineChart, lineChartDataTable, lineChartOptions,
        tableChart, trainDescr;
        if (_params && _lineChartData && _columnChartData) {
            params = _params;
            lineChartData = _lineChartData;
            columnChartData = _columnChartData;
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
        if (status === 'hidden') {
            return;
        }
        if (status === 'loading') {
            divCtrlList[divIdx.chart1].setAttribute('style', 'display: block;');
            divCtrlList[divIdx.chart1].innerHTML = "loading..";
            return;
        }
        if (!that.getChartsLibReady()) {
            console.log('Surveys, chartsLibReady is false');
            return;
        }
        if (!lineChartData.rows || !columnChartData.rows ||
             lineChartData.rows.length === 0 || columnChartData.rows.length === 0) {
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

        divCtrlList[divIdx.hd1].setAttribute('style', 'display: block;');
        lineChartDataTable = new google.visualization.DataTable(lineChartData);
        lineChartOptions = {
            title: '{{nls.trainNum}} ' + params.type + ' ' + params.trainId +
                   ' {{nls.left}} ' + params.leaveTime + ' {{nls.left_day}} ' +
                   params.selectedDate,
            curveType: 'function',
            legend: {position: 'top',
                     textStyle: { bold: false}},
            tooltip: {trigger: 'selection'}
        };
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
            title: '{{nls.trainNum}} ' + params.type + ' ' + params.trainId +
                   ' {{nls.left}} ' + params.leaveTime + ' {{nls.left_day}} ' +
                   params.selectedDate,
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

    that.hide = function() {
        var tmp, divIdList = proto.divList;
        for (var i = 0; i < divIdList.length; i++) {
            tmp = document.getElementById(divIdList[i]);
            if (!tmp) {
                console.log('Surveys, cannot find div(' + divList[i] +')');
                return;
            }
            tmp.setAttribute('style', 'display: none;');
        };
        status = 'hidden';
    }

    return that.init();
}
{% endautoescape %}
