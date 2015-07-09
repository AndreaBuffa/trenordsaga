var MYAPP = MYAPP || {};
MYAPP.View = MYAPP.View || {};

MYAPP.View.TrainSelector = function(aModel, aControl) {
	this.status = "loading";
	this.myModel = aModel;
	this.notifyControl = aControl;
}

MYAPP.View.TrainSelector.prototype.update = function() {
	var obj = this;
	this.myModel.getTrainList(function(trainList) {
			trainList = trainList || [];
			trainList.sort(function(a, b) {
					var number1 = a.type.match(/(\d+)$/);
					var number2 = b.type.match(/(\d+)$/);
					if (number1 == null) {
						if (number2 == null) {
							return 0;
						} else {
							return -1;
						}
					} else {
						if (number2 == null) {
							return 1;
						} else {
							return parseInt(number1[0]) - parseInt(number2[0]);
						}
					}
				});
			obj.status = "ready";
			obj.draw(trainList);
		});
}

MYAPP.View.TrainSelector.prototype.draw = function(trainList) {
	var container = document.querySelector('#trainSelector');
	if (container) {
		while (container.hasChildNodes()) {
			container.removeChild(container.lastChild);
		}
	} else {
		container = document.createElement('div');
		container.setAttribute('id', 'trainSelector');
		document.querySelector('#outputLog').appendChild(container);
	}
	if (this.status === "loading") {
		container.innerHTML = "Loading....";
	} else {
	      var obj = this;
		var currRailwayType = '';
		var rowDiv;
		for (var i = 0; i < trainList.length; i++) {
			var train = trainList[i];
			if (currRailwayType != train.type) {
				currRailwayType = train.type;
				rowDiv = document.createElement('div');
				rowDiv.classList.add('row');
				var img = document.createElement('img');
				img.src = 'images/' + currRailwayType + '.jpg';
				rowDiv.appendChild(img);
				document.querySelector('#trainSelector').appendChild(rowDiv);
				rowDiv = document.createElement('div');
				rowDiv.classList.add('row');
				document.querySelector('#trainSelector').appendChild(rowDiv);
			}
			var linkControl = document.createElement('a');
			linkControl.setAttribute('id', train.trainId);
			linkControl.setAttribute('surveyedFrom', train.surveyedFrom);
			linkControl.addEventListener('click', function() {
					obj.onClick({'trainId': this.id,
						'dayFilter': 'all',
						'surveyedFrom': this.surveyedFrom});
				});
			linkControl.innerHTML = train.trainId + ' - ' + train.leaveStation + ' (' + train.leaveTime + ') - ' + train.endStation+ ' (' + train.arriveTime + ')';
/*			var linkDiv = document.createElement('div');
			linkDiv.classList.add('row');
			linkDiv.appendChild(linkControl);*/
			rowDiv.appendChild(linkControl);
		}
	}
}


MYAPP.View.TrainSelector.prototype.onClick = function(trainDescriptor) {
	console.log("Train selected, no action");
}
