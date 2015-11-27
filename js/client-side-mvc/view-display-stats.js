var MYAPP = MYAPP || {};
MYAPP.View = MYAPP.View || {};

MYAPP.View.TrainStats = function(proto) {
    var anchor = proto.anchor;
	var filter = "all";
	var myModel = proto.model;
	var status = "loading";
	var surveyedFrom = "";
	var that = COMM.Observer(proto);
	var trainId = 0;

	that.update = function(params) {
		if (!params)
			return 0;

		if (trainId !== params.trainId || filter !== params.dayFilter) {
			status = trainId !== params.trainId ? "tranIdChanged" : "filterChanged";
			trainId = params.trainId;
			filter = params.dayFilter;
			surveyedFrom = params.surveyedFrom;
			myModel.getTrainStats(params.trainId, params.dayFilter, function(stats) {
				stats = stats || [];
				stats.sort(function(a, b) {
						if (a.stationName > b.stationName)
							return 1;
						if (a.stationName < b.stationName)
							return -1;
						return 0;
					});
				status = "ready";
				that.draw(stats);
			});
            //@todo delete me
			this.draw();
		}
	}
	that.draw = function(stats) {
		var container = document.querySelector('#trainStats');
		var statsList = null;
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
			paragraph.innerHTML = 'Ecco le statistiche a partire dal ' + surveyedFrom + ':';
			container.appendChild(paragraph);
			statsList = document.createElement('div');
			statsList.setAttribute('id', 'statsList');
			statsList.classList.add('table-wrapper');
			container.appendChild(statsList);

			var tabClickHandler = function() {
				if (status !== "ready") {
					return;
				}
				that.update({'trainId': trainId,
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
		document.querySelector('#container').appendChild(container);
		if (status !== "ready") {
			var element = document.createElement('div');
			element.classList.add('row');
			element.innerHTML = "Loading...";
			statsList.appendChild(element);
		} else {
			var table = document.createElement('table');
			statsList.appendChild(table);
			var thead = document.createElement('thead');
			var trHead = document.createElement('tr');
			var th1 = document.createElement('th');
			th1.innerHTML = 'Stazione';
			var th2 = document.createElement('th');
			th2.innerHTML = 'Ritardo mediano in minuti';
			trHead.appendChild(th1);
			trHead.appendChild(th2);
			thead.appendChild(trHead);
			table.appendChild(thead);
			var tbody = document.createElement('tbody');
			table.appendChild(tbody);
			for (var i = 0; i < stats.length; i++) {
				var stop = stats[i];
				var dataTr = document.createElement('tr');
				//element.classList.add('row');
				var dataTd1 = document.createElement('td');
				dataTd1.innerHTML = stop.stationName;
				var dataTd2 = document.createElement('td');
				dataTd2.innerHTML = stop.median;
				dataTr.appendChild(dataTd1);
				dataTr.appendChild(dataTd2);
				tbody.appendChild(dataTr);
			}
		}
	}
	that.trigger = function(eventName, params) {
		// COMM.event.modelReady
		switch(eventName) {
			case COMM.event.trainChanged:
				this.update(params);
			break;
		}
	}

	return that;
}
