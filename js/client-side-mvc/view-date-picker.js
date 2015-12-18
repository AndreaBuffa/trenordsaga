var MYAPP = MYAPP || {};
MYAPP.View = MYAPP.View || {};

MYAPP.View.DatePicker = function(proto) {
    var currDate, params, status, that;
    params = {};
    status = "loading";
    that = COMM.Notifier(COMM.Observer(proto));

    that.trigger = function(eventName, eventParams) {
        switch(eventName) {
            case COMM.event.trainChanged:
                if (status === "loading") {
                    console.log("Datepicker,(" + eventName + ") received but I'm still loading");
                }
                params = eventParams;
                this.draw();
            break;
        }
    };

    that.draw = function() {
        var container = document.querySelector('#' + proto.divId), div, today;
        if (container) {
            while (container.hasChildNodes()) {
                container.removeChild(container.lastChild);
            }
        } else {
            console.log('Type-Picker, cannot find div container ' + proto.divId);
            return;
        }
        div = document.createElement('div');
        div.innerHTML = '<header class="major"><p>Scegli il giorno:</p></header>';
        container.appendChild(div);

        div = document.createElement('div');
        div.setAttribute('id', 'datepicker');
        container.appendChild(div);

        if (status === 'ready') {
            today = new Date();
            $("[id^=datepicker]").datepicker({
                dateFormat: "yy-mm-dd",
                minDate: params.surveyedFrom,
                maxDate: new Date(today.getFullYear(),
                          today.getMonth(),
                          today.getDate() - 1),
                //defaultDate: currDate,
                onSelect: function(selectedDate) {
                              params.selectedDate = selectedDate;
                              that.notify(COMM.event.dateChanged, params);
                          }
            });
            status = 'ok';
        } else {
            $("[id^=datepicker]").datepicker("option", "minDate",
                                             params.surveyedFrom);
        }
    }

    that.init = function() {
        var head, script = document.createElement("script");
        script.async = true; //useless maybe
        script.setAttribute('src', '//ajax.googleapis.com/ajax/libs/jqueryui/1.11.3/jquery-ui.min.js');
        script.onload = function() {
            status = 'ready';
        }
        head = document.getElementsByTagName('head')[0];
        head.appendChild(script);
        return that;
    }

    return that.init();
}
