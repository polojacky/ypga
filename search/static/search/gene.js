$(function () {

    // get current sort option
    $('th[name]').css('background-image', 'url(/static/images/up_down.gif)');
    var url = location.search;
    var paraString = url.substring(1, url.length).split('&');
    for (var i = 0; i < paraString.length; i++) {
        var parms = paraString[i].split('=');
        if (parms[0] == 'order_by')  //get the order_by parm
        {
            var parm = parms[1];
            if (parms[1].substring(0, 1) == '-') {
                parm = parms[1].substring(1, parms[1].length);
                $('th[name=' + parm + ']').css('background-image', 'url(/static/images/down.gif)');
            } else {
                $('th[name=' + parm + ']').css('background-image', 'url(/static/images/up.gif)');
            }

            //change the opacity
            $('img[name=' + parms[1] + ']').css('opacity', '0.1');
        }
    }
});


//select all rows of current page
function selectCurrentPage(item) {
    $("input[name='tableRowCheckBox']").prop("checked", $(item).prop("checked"));
    if ($(item).prop("checked") == false) {
        $('#selectAllPage').prop("checked", false);
    }
    updateSelectNumber();
}

//select rows of all pages, including those not displayed
//it seems that it is the same with selectCurrentPage, we will check the state of this checkbox
function selectAllPage(item) {
    $('#selectCurrentPage').prop("checked", $(item).prop("checked"));
    $("input[name='tableRowCheckBox']").prop("checked", $(item).prop("checked"));
    updateSelectNumber();
}

//check if not all selected, just uncheck the selectCurrentPage and selectAllPageCheckbox
function stillSelectAll(item) {
    if ($(item).prop("checked") == false) {
        $('#selectCurrentPage').prop("checked", false);
        $('#selectAllPage').prop("checked", false);
    }
    updateSelectNumber();
}

//update select number
function updateSelectNumber() {
    var number = 0
    if ($('#selectAllPage').prop("checked") == true) {  //all pages
        number = $('#interactions').text();
    } else {
        $("input[name='tableRowCheckBox']").each(function (row) {
            if ($(this).prop("checked") == true) {
                number += 1;
            }
        });
    }
    $('#selectNumber').text(number);
    selectedNumber = number;
}

//number of selected row
selectedNumber = 0;

//advanced result page
function performFunction(item) {

    //first check is there any data selected
    //var selectedNumber = $('#selectNumber')
    if (selectedNumber > 0) {
        //check the state of select
        var functionType = item;
        if (functionType == "download") {  //download data
            var selected;
            var type
            //get the selected items
            if ($('#selectAllPage').prop("checked")) {  //select all rows
                selected = $('#strain').text();
                type = 'all'
            } else {  //only current page
                selected = new Array();
                $("input[name='tableRowCheckBox']").each(function () {
                    if ($(this).prop("checked")) {
                        selected.push($(this).val());
                    }
                });
                type = 'current';
            }

            $.fileDownload('/search/gene/download/?selected=' + selected + '&type=' + type)
                .done(function () {
                })
                .fail(function () {
                    alert('File download failed!');
                });

        }
    } else {
        $('#selectAllPage').popover({content: 'please select a record'});
        $('#selectAllPage').popover('show');
        setTimeout(function () {
            $('#selectAllPage').popover('destroy');
        }, 3000);
    }


}
