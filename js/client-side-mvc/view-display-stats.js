var MYAPP = MYAPP || {};
MYAPP.View = MYAPP.View || {};

MYAPP.View.TrainStats = function(aModel) {
	this.status = "loading";
	this.myModel = aModel;
	this.trainId = 0;
	this.filter = "all";
}

MYAPP.View.TrainStats.prototype.update = function(params) {
	if (!params)
		return 0;

	var thisObj = this;
	if (this.trainId !== params.trainId || this.filter !== params.dayFilter) {
		this.status = this.trainId !== params.trainId ? "tranIdChanged" : "filterChanged";
		this.trainId = params.trainId;
		this.filter = params.dayFilter;
		this.surveyedFrom = params.surveyedFrom;
		this.myModel.getTrainStats(params.trainId, params.dayFilter, function(stats) {
			stats = stats || [];
			stats.sort(function(a, b) {
					if (a.stationName > b.stationName)
						return 1;
					if (a.stationName < b.stationName)
						return -1;
					return 0;
				});
			thisObj.status = "ready";
			thisObj.draw(stats);
			});
		this.draw();
	}
}

MYAPP.View.TrainStats.prototype.draw = function(stats) {
	var container = document.querySelector('#trainStats');
	var statsList = null;
	if (container) {
		statsList = document.querySelector('#statsList');
		while (statsList.hasChildNodes()) {
			statsList.removeChild(statsList.lastChild);
		}
		if (this.status === 'tranIdChanged') {
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
		paragraph.innerHTML = 'In rilevazione dal ' + this.surveyedFrom;
		container.appendChild(paragraph);
		statsList = document.createElement('div');
		statsList.setAttribute('id', 'statsList');
		statsList.classList.add('table-wrapper');
		container.appendChild(statsList);

		var thisObj = this;
		var tabClickHandler = function() {
			if (thisObj.status !== "ready") {
				return;
			}
			thisObj.update({'trainId': thisObj.trainId,
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
	document.querySelector('#outputLog').appendChild(container);
	if (this.status !== "ready") {
		var element = document.createElement('div');
		element.classList.add('row');
		element.innerHTML = "Loading...";
		statsList.appendChild(element);
	} else {
		table = document.createElement('table');
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
