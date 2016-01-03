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
                /* Italian initialisation for the jQuery UI date picker plugin. */
                /* Written by Antonello Pasella (antonello.pasella@gmail.com). */
                ( function( factory ) {
                    if ( typeof define === "function" && define.amd ) {

                        // AMD. Register as an anonymous module.
                        define( [ "../widgets/datepicker" ], factory );
                    } else {

                        // Browser globals
                        factory( jQuery.datepicker );
                    }
                }( function( datepicker ) {

                datepicker.regional.it = {
                    closeText: "Chiudi",
                    prevText: "&#x3C;Prec",
                    nextText: "Succ&#x3E;",
                    currentText: "Oggi",
                    monthNames: [ "Gennaio","Febbraio","Marzo","Aprile","Maggio","Giugno",
                        "Luglio","Agosto","Settembre","Ottobre","Novembre","Dicembre" ],
                    monthNamesShort: [ "Gen","Feb","Mar","Apr","Mag","Giu",
                        "Lug","Ago","Set","Ott","Nov","Dic" ],
                    dayNames: [ "Domenica","Lunedì","Martedì","Mercoledì","Giovedì","Venerdì","Sabato" ],
                    dayNamesShort: [ "Dom","Lun","Mar","Mer","Gio","Ven","Sab" ],
                    dayNamesMin: [ "Do","Lu","Ma","Me","Gi","Ve","Sa" ],
                    weekHeader: "Sm",
                    dateFormat: "dd/mm/yy",
                    firstDay: 1,
                    isRTL: false,
                    showMonthAfterYear: false,
                    yearSuffix: "" };
                datepicker.setDefaults( datepicker.regional.it );

                return datepicker.regional.it;

                } ) );
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
        div.innerHTML = '<h2>Scegli il giorno:</h2>';
        container.appendChild(div);

        div = document.createElement('div');
        div.setAttribute('id', 'datepicker');
        container.appendChild(div);

        if (status === 'ready') {
            today = new Date();
            $("#datepicker").datepicker({
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
