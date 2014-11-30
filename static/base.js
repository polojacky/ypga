/**
 * Created by jacky on 14-3-10.
 */

$(document).ready(function () {
    /*
     update the navbar status, based on the url pattern
     * */
    var position = window.location.pathname;
    var idx1 = position.indexOf('/', 1);
    if (idx1 < 0) {  // ehfpi
        $('#home').addClass('active');
    } else {
        var idx2 = position.indexOf('/',idx1+1);
        if(idx2 < 0){
            $('#home').addClass('active');  // ehfpi/
        }else{

            var posName = position.substr(idx1+1, idx2 - idx1-1);
            if (posName == 'rest') { //in download now
                $('#download').addClass('active');
            } else {
                $('#' + posName).addClass('active');
            }
        }
    }

    //clear search using jquery-clearsearch
    //$('input[name=query]').clearSearch();

});


