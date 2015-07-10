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
	      for (var i = 0; i < stats.length; i++) {
			var stop = stats[i];
			var element = document.createElement('div');
			//element.classList.add('row');
			element.innerHTML = stop.stationName + ' : ' + stop.median;
			statsList.appendChild(element);
	      }
	}
}
