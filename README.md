This repo has two main purposes:
- to trace some railways line delays and generate statistics
- to improve my Python

Features:
- implemented in my spare time and still in progress.
- implement MVC.
- expose REST API for accessing surveys and statistics (median).
- made of both synchronous and asynchronous pages.
- implement a simple national language support system.
- use messaging for third-party data retrieval
- use the NoSQL Google datastore, abstracted by a factory.
- built on top of the Google Cloud Platform using webapp2.
- use third-party HTML/CSS template.

API REST

- GET api/surveys/v1/list
- GET api/surveys/v1/survey/{trainId}/{year}/{month}/{day}
- GET api/surveys/v1/source/{trainId}/2016/02/17
- GET api/surveys/v1/search/{fromStation}/{toStation}/{when}/{timeRange}
- POST api/surveys/v1/survey/add/{fromStation}/{toStation}/{when}/{timeRange}
- GET api/surveys/v1/stats/{trainId}



