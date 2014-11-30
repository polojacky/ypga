//accordion for parameter
$(function () {

});

var oTimer = null;
jQuery(document).ready(function () {
    var jobId = $('#jobId').text()
    oTimer = setInterval(function () {
        queryState(jobId);
    }, 5000);
});

function queryState(jobId) {
    $.getJSON('/tools/ajaxQueryState', {'jobId': jobId}, function (json) {
        console.log(json);
        var state = json.state;
        var msg = json.msg;
        console.log(state);
        console.log(msg);
        if (state == 'COMPLETE') {
            document.getElementById('loading').innerHTML = msg;
            window.clearInterval(oTimer);
        } else if (state == 'FAILED') {
            document.getElementById('loading').innerHTML = msg;
            window.clearInterval(oTimer);
        } else {
            //do nothing
        }

    })
}



