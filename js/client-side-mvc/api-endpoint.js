// requires the global myModel
function init() {
	//var apiRoot = 'https://disco-parsec-749.appspot.com/_ah/api';
	var apiRoot = 'http://localhost:8080/_ah/api';
	var apisToLoad;
	var APIReady = function(tmp) {
		if (--apisToLoad == 0) {
			model.ready();
		}
	}
	apisToLoad = 1;
	gapi.client.load('surveys', 'v1', APIReady, apiRoot);
}
</script>
<script async src="https://apis.google.com/js/client.js?onload=init"></script>
