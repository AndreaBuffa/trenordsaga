var MYAPP = MYAPP || {};
MYAPP.View = MYAPP.View || {};

MYAPP.View.TrainStats = function(that) {
    var anchor = that.anchor, drawTableFun, graphData, myModel = that.model,
    params, rowData, status = "loading";
    drawTableFun = function(_stats) {
        var chartDiv, columnChart, delays = [], counters = [], data, dataTd1,
        dataTd2, dataTr, stop, table, tbody, th1, th2, thead;
        table = document.createElement('table');
        thead = document.createElement('thead');
        trHead = document.createElement('tr');
        th1 = document.createElement('th');
        th1.innerHTML = 'Stazione';
        th2 = document.createElement('th');
        th2.innerHTML = 'Ritardo mediano in minuti';
        trHead.appendChild(th1);
        trHead.appendChild(th2);
        thead.appendChild(trHead);
        table.appendChild(thead);
        tbody = document.createElement('tbody');
        table.appendChild(tbody);
        for (var i = 0; i < _stats.length; i++) {
            stop = _stats[i];
            dataTr = document.createElement('tr');
            dataTd1 = document.createElement('td');
            dataTd1.innerHTML = stop.stationName;
            dataTd2 = document.createElement('td');
            chartDiv = document.createElement('div');
            dataTd2.appendChild(chartDiv);
            data = new google.visualization.DataTable();
            data.addColumn('string', 'delay');
            data.addColumn('number', 'times happened');
            switch (params.dayFilter) {
                case "workDay":
                    //dataTd2.innerHTML = stop.weekdayMedian;
                    delays = stop.weekdaySamples;
                    counters = stop.weekdayCounters;
                    break;
                case "dayOff":
                    //dataTd2.innerHTML = stop.festiveMedian;
                    delays = stop.festiveSamples;
                    counters = stop.festiveCounters;
                    break;
                case "all":
                    //dataTd2.innerHTML = stop.allMedian;
                    delays = stop.allSamples;
                    counters = stop.allCounters;
                    break;
            }
            /*var dt = new google.visualization.DataTable({
                cols: [{id: 'task', label: 'Task', type: 'string'},
                       {id: 'hours', label: 'Hours per Day', type: 'number'}],
                rows: [{c:[{v: 'Work'}, {v: 11}]},
                       {c:[{v: 'Eat'}, {v: 2}]},
                       {c:[{v: 'Commute'}, {v: 2}]},
                       {c:[{v: 'Watch TV'}, {v:2}]},
                       {c:[{v: 'Sleep'}, {v:7, f:'7.000'}]}]
                }, 0.6);

            data.addRows([
              ['Work', 11],
              ['Eat', 2],
              ['Commute', 2],
              ['Watch TV', 2],
              ['Sleep', {v:7, f:'7.000'}]
            ]);*/
            for (var j = 0; j < delays.length; j++) {
                data.insertRows(j, new Array([delays[j], parseInt(counters[j])]));
            };
            columnChart = new google.visualization.ColumnChart(chartDiv);
            var samplesChartOpt = {
                title: '{{nls.trainNum}} ' + params.trainType + ' ' + params.trainId +
                   ' {{nls.left}} ' + params.leaveTime,
                /*chartArea: {'width': '85%'},*/
                legend: {position: 'top', textStyle: { bold: false}},
                tooltip: {trigger: 'selection'}
            };
            columnChart.draw(data, samplesChartOpt);
            dataTr.appendChild(dataTd1);
            dataTr.appendChild(dataTd2);
            tbody.appendChild(dataTr);
        }
        return table;
    };
    that = COMM.Observer(that);
    that = COMM.GChartsLibInit(that, function(){});
    that = COMM.DrawOnResize(that);

    that.update = function(_params) {
        if (!_params)
            return 0;
        if (!params) {
            params = _params;
        }

        if (params.trainId !== _params.trainId || params.filter !== _params.dayFilter) {
            params = _params;
            status = "ready";

            myModel.getStats(params.trainId, function(graphData, rowData) {
                that.draw(graphData, rowData);
            });
        }
    };

    that.draw = function(_graphData, _rowData) {
        if (_graphData && _rowData) {
            graphData = _graphData;
            rowData = _rowData;
        }
        that.drawGraph(graphData);
        that.drawTable(rowData);
    };

    that.drawTable = function(stats) {
        var container = document.querySelector('#trainStats'), drawTable, statsList = null;

        if (container) {
            statsList = document.querySelector('#statsList');
            while (statsList.hasChildNodes()) {
                statsList.removeChild(statsList.lastChild);
            }
            if (status === 'tranIdChanged') {
                document.querySelector('#all').classList.add('active');
                document.querySelector('#workDay').classList.remove('active');
                document.querySelector('#dayOff').classList.remove('active');
            }
        } else {
            container = document.createElement('div');
            container.setAttribute('id', 'trainStats');
            container.innerHTML = '<ul id="tabs"><li id="all" class="active">tutte</li>\
                <li id="workDay">feriali</li><li id="dayOff">festivi</li></ul>';
            var paragraph = document.createElement('p');
            paragraph.innerHTML = 'Statistiche a partire dal ' + params.surveyedFrom + ':';
            container.appendChild(paragraph);
            statsList = document.createElement('div');
            statsList.setAttribute('id', 'statsList');
            statsList.classList.add('table-wrapper');
            container.appendChild(statsList);

            var tabClickHandler = function() {
                if (status !== "ready") {
                    return;
                }
                that.update({'trainId': params.trainId,
                        'dayFilter': this.id});

                for(var i=0; i < this.parentElement.childElementCount; i++) {
                    if (this.parentElement.children[i] === this) {
                        this.parentElement.children[i].classList.add('active');
                    } else {
                        this.parentElement.children[i].classList.remove('active');
                    }
                }
            };
            var tmp = container.querySelector('#all');
            tmp.addEventListener('click', tabClickHandler);
            var tmp = container.querySelector('#dayOff');
            tmp.addEventListener('click', tabClickHandler);
            var tmp = container.querySelector('#workDay');
            tmp.addEventListener('click', tabClickHandler);
        }
        if (document.querySelector('#' + that.divId)) {
            document.querySelector('#' + that.divId).appendChild(container);
            document.querySelector('#' + that.divId).setAttribute('style', 'display: block;');
        } else {
            console.log('TrainStats, cannot find the main div cont.' + that.divId);
            return;
        }
        if (status !== "ready") {
            var element = document.createElement('div');
            element.classList.add('row');
            element.innerHTML = "Loading...";
            statsList.appendChild(element);
        } else {
            statsList.appendChild(drawTableFun(stats));
        }
    };

    that.drawGraph = function(stats) {
        var chart, graphDiv, dataTable, options;
        graphDiv = document.querySelector('#statsGraph');
        if (!graphDiv) {
            graphDiv = document.createElement('div');
            graphDiv.setAttribute('id', 'statsGraph');
            graphDiv.setAttribute('class', 'lineChart');
            document.querySelector('#' + that.divId).appendChild(graphDiv);
        }
        dataTable = new google.visualization.DataTable(stats);
        //params.trainId
        options = {
            title: '{{nls.trainNum}} ' + params.trainType + ' ' + params.trainId +
                   ' {{nls.been_surveyed}} ' + params.surveyedFrom,
            chartArea: {'width': '85%'},
            legend: {position: 'top',
                     textStyle: { bold: false}},
            tooltip: {trigger: 'selection'}
        };
        chart = new google.visualization.ColumnChart(graphDiv);
        chart.draw(dataTable, options);
    };

    that.trigger = function(eventName, params) {
        switch(eventName) {
            case COMM.event.trainChanged:
                this.update(params);
            break;
            case COMM.event.tabChanged:
                if (params.visible === false) {
                    //that.hide();
                }
            break;
        }
    };

    that.hide = function() {
        var container = document.querySelector('#' + that.divId);
        if (!container) {
            console.log('Stats, cannot find div(' + that.divId +')');
            return;
        }
        container.setAttribute('style', 'display: none;');
    };

    return that;
};
