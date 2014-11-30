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

    //filter preset
    var types = $('#types').text().split(',');
    var strains = $('#strains').text().split(',');
    console.log(types);
    console.log(strains);
    for(var j=0;j<types.length;j++){
        if(types[j]!=''){
            $("input[name='type'][id='"+types[j]+"']").prop("checked",true);
        }
    }

    for(var j=0;j<strains.length;j++){
        if(strains[j]!=''){
            $("input[name='strain'][id='"+strains[j]+"']").prop("checked",true);
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


function selectAllStrain(item) {

    $('#selectAllStrain').prop("checked", $(item).prop("checked"));
    $("input[name='strain']").prop("checked", $(item).prop("checked"));
}

function stillSelectStrainAll(item) {
    if ($(item).prop("checked") == false) {
        $('#selectAllStrain').prop("checked", false);
    }
}

function selectAllType(item) {

    $('#selectAllType').prop("checked", $(item).prop("checked"));
    $("input[name='type']").prop("checked", $(item).prop("checked"));
}

function stillSelectTypeAll(item) {
    if ($(item).prop("checked") == false) {
        $('#selectAllType').prop("checked", false);
    }
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

function checkEmpty() {

    var selected1 = 0;
    var text = $("#geneList").val().replace(/(^\s*)|(\s*$)/g, '');  //remove space
    if (text.length > 0) {
        selected1 = 1;
    }

    if (selected1 == 0) {
        //popover hint
        $('#snpAnalysis').popover({content: 'please input id list'});
        $('#snpAnalysis').popover('show');
        setTimeout(function () {
            $('#snpAnalysis').popover('destroy');
        }, 3000);
        return false;

    } else {
        return true;
    }

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
            var selected = new Array();
            //get the selected items
            if ($('#selectAllPage').prop("checked")) {  //select all rows
                selected = $('#geneList').text().split(',');
            } else {  //only current page
                $("input[name='tableRowCheckBox']").each(function () {
                    if ($(this).prop("checked")) {
                        selected.push($(this).val());
                    }
                });
            }

            var csrf = $('#csrf').attr("value");
            var index = csrf.indexOf('value=');
            var index2 = csrf.lastIndexOf("'");
            var csrfmiddlewaretoken = csrf.substr(index + 7, index2 - index - 7);

            $.fileDownload('/tools/homology/download/', {
                httpMethod: "POST",
                data: {
                    selected: selected,
                    csrfmiddlewaretoken: csrfmiddlewaretoken
                }

            })
                .done(function () {
                })
                .fail(function () {
                    alert('File download failed!');
                });

        } else if (functionType == "network") {
            var geneList;
            var sum = 0;
            //get the selected items
            if ($('#selectAllPage').prop("checked")) {  //select all rows
                geneList = $('#geneList').text();
                sum = $('#sum').text();
            } else {  //only current page
                var arr = new Array();
                $("input[name='tableRowCheckBox']").each(function () {
                    if ($(this).prop("checked")) {
                        arr.push($(this).val());
                    }
                });

                geneList = arr.join(',');
            }
            if (sum < 400) {
                openPostWindow('/tools/homologyView/', geneList, '/search/homologyView/');
            } else {
                $('#selectAllPage').popover({content: "Correspond list too long!"});
                $('#selectAllPage').popover('show');
                setTimeout(function () {
                    $('#selectAllPage').popover('destroy');
                }, 3000);
            }
        } else {

        }
    } else {
        $('#selectAllPage').popover({content: 'please select a record'});
        $('#selectAllPage').popover('show');
        setTimeout(function () {
            $('#selectAllPage').popover('destroy');
        }, 3000);
    }

}

types = new Array();
//custom filter columns
function filterTable(item) {
    types.length = 0; //empty the array
    $("input[name ='type']").each(function () {
        if ($(this).prop("checked")) {
            types.push($(this).val());
        }
    });

    //parse url address, same in search change columns
    var url = window.location.search.substr(1);
    var urlList = url.split("&");
    //console.log(urlList);
    var columnIn = 0;
    for (var i = 0; i < urlList.length; i++) {
        var index = urlList[i].indexOf('=');
        var myKey = urlList[i].substr(0, index);
        if (myKey == 'types') {  //in the url
            columnIn = 1;
            urlList[i] = 'types=' + types;
            break;
        }
    }
    if (columnIn == 0) {
        if (url.length > 0) {
            url = window.location.href + '&types=' + types;
        } else {
            url = window.location.href + '?types=' + types;
        }
    } else {
        url = window.location.pathname + '?' + urlList.join("&");
    }
    //console.log(url);
    window.location.href = url;
}

//post into a new window
function openPostWindow(url, data, name) {
    var tempForm = document.createElement("form");
    tempForm.id = "tempForm1";
    tempForm.method = "post";
    tempForm.action = url;
    tempForm.target = name;

    var hideInput = document.createElement("input");
    hideInput.type = "hidden";
    hideInput.name = "geneList"
    hideInput.value = data;
    tempForm.appendChild(hideInput);

    $(tempForm).append($('#csrf').attr("value"));


    //open new window first
    openWindow(name);

    document.body.appendChild(tempForm);
    tempForm.submit();
    document.body.removeChild(tempForm);
}

function openWindow(name) {
    window.open('about:blank', name);
}


strains = new Array();
//ajax call filter the table content
function filterResult(data) {
    types.length = 0; //empty the array
    strains.length = 0;

    $("input[name ='type']").each(function () {
        if ($(this).prop("checked")) {
            types.push($(this).val());
        }
    });

    $("input[name ='strain']").each(function () {
        if ($(this).prop("checked")) {
            strains.push($(this).val());
        }
    });

    //parse url address, same in search change columns
    var url = window.location.search.substr(1);
    var urlListTmp = url.split("&");
    var urlList = new Array()
    for (var j = 0; j < urlListTmp.length; j++) {
        if (urlListTmp[j] != '') {
            urlList.push(urlListTmp[j])
        }
    }

    //console.log(urlList);
    var columnIn1 = 0;
    var columnIn2 = 0;
    console.log(urlList);
    for (var i = 0; i < urlList.length; i++) {
        var index = urlList[i].indexOf('=');
        var myKey = urlList[i].substr(0, index);
        if (myKey == 'types') {  //in the url
            columnIn1 = 1;
            if (types.length > 0) {
                urlList[i] = 'types=' + types;
            } else {
                urlList[i] = '';
            }
        }
        if (myKey == 'strains') {  //in the url
            columnIn2 = 1;
            if (strains.length > 0) {
                urlList[i] = 'strains=' + strains;
            } else {
                urlList[i] = '';
            }
        }
    }

    if (columnIn1 == 0 && types.length > 0) {
        urlList.push('types=' + types);
    }

    if (columnIn2 == 0 && strains.length > 0) {
        urlList.push('strains=' + strains);
    }

    var urlFinal = new Array()
    for (var j = 0; j < urlList.length; j++) {
        if (urlList[j] != '') {
            urlFinal.push(urlList[j])
        }
    }

    url = window.location.pathname + '?' + urlFinal.join("&");

    console.log(url);
    window.location.href = url;


}