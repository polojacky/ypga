var text = '<div class="displayNetwork">\
    <div class="row ">\
        <div class="col-md-3">\
            <div class="geneStat">\
                    <span class="geneStatTitle">Gene Summary</span>\
                    <span id="networkTip2"><a href="/ehfpi/help/analysisHelp#network" %} target="_blank"><img\
                    src="/static/images/info_20x20.png"></a></span><br/ >\
            </div>\
            <div class="searchCenter">\
                <div class="searchNetwork">\
                    Search graph:\
                    <div class="searchInput">\
                        <input type="text" class="form-control" id="searchNet" name="searchNet"\
                               placeholder="Search a gene" onkeydown="keyDown(event);">\
                    </div>\
                    <input type="button" value="Search" id ="searchButton" class="btn btn-primary btn-sm" onclick="searchNet(this);">\
                </div>\
            </div>\
            <div class="connections" id="connections">\
                <b>Connections</b>:\
                <div id="inner-detail" contenteditable="true"></div>\
            </div>\
        </div>\
        <div class="col-md-9">\
            <div class="center-panel">\
                <div class="download"><label id="download" onclick="download(this);">Save as image</label></div>\
                <div id="zoomWrapper">\
                    <table>\
                        <tr>\
                            <td>\
                                <button id="zoomin" class="btn btn-sm btn-info" type="button" onclick="zoomin(this);">zoom in</button>\
                            </td>\
                            <td>\
                                <div id="zoom"></div>\
                            </td>\
                            <td>\
                                <button id="zoomout" class="btn btn-sm btn-info" type="button" onclick="zoomout(this);">zoom out</button>\
                            </td>\
                        </tr>\
                    </table>\
                </div>\
                <div id="log"></div>\
                <div id="infovis"></div>\
            </div>\
            <div class="legend_div" id="legend_div">\
            </div>\
        </div>\
    </div>\
</div>';
document.getElementById("main").innerHTML = text;

// init data
var json_ori = '{{toJson}}';
var json = json_ori.replace(/&quot;/g, '\"');  // replace html &quot; with "
var evalJson = eval("(" + json + ")");
init(evalJson);


