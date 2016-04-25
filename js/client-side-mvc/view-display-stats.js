var MYAPP = MYAPP || {};
MYAPP.View = MYAPP.View || {};

MYAPP.View.TrainStats = function(that) {
    var anchor = that.anchor, drawTableFun, graphData, mode = 0, mean, median,
    myModel = that.model, params, rowData,
    status, stateId, tpl1 = "<div><table><thead><th colspan='2'>",
    tpl2 = "</th></thead><tbody><tr><td>Moda</td><td>",
    tpl3 = "&nbsp;minuti</td></tr><tr><td>Mediana</td><td>",
    tpl4 = "&nbsp;minuti</td></tr><tr><td>Media</td><td>",
    tpl5 = "&nbsp;minuti</td></tr></tbody></table></div>";
    stateId = {'hidden': 0, 'ready': 1, 'loading': 2};
    status = stateId.hidden;
    drawTableFun = function(_stats) {
        var accum = 0, chartDiv, columnChart, counter = 0, delay = 0, delays = [],
        counters = [], data, dataTd1, dataTd2, dataTr, maxCounter = 0, stop,
        table, tbody, th1, th2, thead, totCounter = 0;
        table = document.createElement('table');
        /*thead = document.createElement('thead');
        trHead = document.createElement('tr');
        th1 = document.createElement('th');
        th1.innerHTML = 'Stazione';
        th2 = document.createElement('th');
        th2.innerHTML = 'Ritardo mediano in minuti';
        trHead.appendChild(th1);
        trHead.appendChild(th2);
        thead.appendChild(trHead);
        table.appendChild(thead);*/
        tbody = document.createElement('tbody');
        table.appendChild(tbody);
        for (var i = 0; i < _stats.length; i++) {
            stop = _stats[i];
            dataTr = document.createElement('tr');
            /*dataTd1 = document.createElement('td');
            dataTd1.innerHTML = stop.stationName;
            dataTr.appendChild(dataTd1);*/
            dataTd2 = document.createElement('td');
            chartDiv = document.createElement('div');
            dataTd2.appendChild(chartDiv);

            switch (params.dayFilter) {
                case "workDay":
                    delays = stop.weekdaySamples;
                    counters = stop.weekdayCounters;
                    median = stop.weekdayMedian;
                    break;
                case "dayOff":
                    delays = stop.festiveSamples;
                    counters = stop.festiveCounters;
                    median = stop.festiveMedian;
                    break;
                case "all":
                    delays = stop.allSamples;
                    counters = stop.allCounters;
                    median = stop.allMedian;
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

            data = new google.visualization.DataTable();
            data.addColumn('string', 'delay');
            data.addColumn('number', '{{ nls.surveyed }}');
            totCounter = accum = 0;
            for (var j = 0; j < delays.length; j++) {
                counter = parseInt(counters[j]);
                delay = parseInt(delays[j]);
                totCounter += counter;
                accum += delay * counter;
                if (counter > maxCounter) {
                    maxCounter = counter;
                    mode = delay;
                }
            };
            for (var j = 0; j < delays.length; j++) {
                counter = parseInt(counters[j]);
                //f:(delays[j] < 2 ? delays[j] + '{{ nls.minute }}' : delays[j] + '{{ nls.minutes }}')
                data.insertRows(j, new Array([
                    delays[j],
                    {v: counter, f: counter + ' volte su ' + totCounter}]));
            };
            mean = (totCounter === 0) ? 0 : Math.floor(accum / totCounter);
            dataTd2.innerHTML = tpl1 + stop.stationName + tpl2 + mode + tpl3 +
                median + tpl4 + mean + tpl5;
            test = document.createElement('div');
            test.setAttribute('id', 'sampleChart');
            dataTd2.appendChild(test);
            dataTr.appendChild(dataTd2);
            tbody.appendChild(dataTr);
            columnChart = new google.visualization.ColumnChart(test);
            var samplesChartOpt = {
                title: stop.stationName + '({{nls.trainNum}} ' + params.trainType +
                    ' ' + params.trainId + ')' + params.leaveTime,
                /*chartArea: {'width': '85%'},*/
                legend: {position: 'top',
                         textStyle: { bold: false}},
                hAxis: {title: '{{ nls.surveyed_del }}'}
            };
            columnChart.draw(data, samplesChartOpt);
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
            status = stateId.ready;

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
            if (status === stateId.tranIdChanged) {
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
                if (status !== stateId.ready) {
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
        if (status !== stateId.ready) {
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

    that.trigger = function(eventName, _params) {
        switch(eventName) {
            case COMM.event.trainChanged:
                this.update(_params);
            break;
            case COMM.event.tabChanged:
                that.toggleDisplay(_params.visible);
            break;
        }
    };

    that.toggleDisplay = function(visible) {
        var tmp, statusList;
        if (!visible) {
            displayMemento = [];
        }
        tmp = document.getElementById(that.divId);
        if (!tmp) {
            console.log('Stats, cannot find div(' + divList[i] +')');
            return;
        }
        if (visible) {
            tmp.setAttribute('style', displayMemento[i]);
        } else {
            displayMemento.push(tmp.getAttribute('style'));
            tmp.setAttribute('style', 'display: none;');
        }
        status = visible === true ? stateId.ready: stateId.hidden;
    };

    return that;
};
