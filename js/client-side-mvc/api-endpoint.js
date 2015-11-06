// requires the global myModel
function init() {
	var apiRoot = 'https://disco-parsec-749.appspot.com/_ah/api';
	//var apiRoot = 'http://localhost:8080/_ah/api';
	var apisToLoad;
	var APIReady = function() {
		if (--apisToLoad == 0) {
			myModel.ready();
		}
	}
	apisToLoad = 3;
	gapi.client.load('discover', 'v1', APIReady, apiRoot);
	gapi.client.load('statistics', 'v1', APIReady, apiRoot);
	gapi.client.load('schedule', 'v1', APIReady, apiRoot);
}
</script>
<script async src="https://apis.google.com/js/client.js?onload=init"></script>
