$(function () {
    //scribl
    draw('canvas');
});

//return the position of the given id
function getPosition(pos) {
    var position = new Array();
    var postmp = pos.substr(pos.lastIndexOf(':') + 1);
    var pos1 = postmp.substr(0, postmp.indexOf('-'));

    var dir = '+';
    if (pos1[0] == 'c') {
        dir = '-';
        pos1 = pos1.substr(1);
    }

    var pos2 = postmp.substr(postmp.indexOf('-') + 1);
    position.push(dir);
    position.push(parseInt(pos1));
    position.push(parseInt(pos2));
    return position;
}

function draw(canvasName) {

    // Get Canvas and Create Chart
    var canvas = document.getElementById(canvasName);
    canvas.width = 800;
    canvas.height = 200;

    // Create Chart
    var chart1 = new Scribl(canvas, 600);

//    chart1.scale.min = 100000;
//    chart1.scale.max = 120000;
    chart1.scale.font.color = "#00008B";
    chart1.scale.font.size = 16;
    chart1.scale.size = 10;

    chart1.glyph.color = 'lightblue';
    chart1.glyph.text.color = 'darkred';
    chart1.glyph.text.size = '14'; // in pixels
    chart1.glyph.text.font = 'Lucida Grande';
    chart1.glyph.text.align = 'center';

    chart1.tooltips = {};
    chart1.tooltips.text = {}
    chart1.tooltips.text.font = 'Lucida Grande';
    chart1.tooltips.text.size = 14; // in pixels
    chart1.tooltips.borderWidth = 1; // in pixels
    chart1.tooltips.roundness = 3;  // in pixels
    chart1.tooltips.fade = true;
    chart1.tooltips.style = 'light';  // also a 'dark' option


    var idintergenic = $('#idintergenic').text();
    var upstreamgeneid = $('#upstreamgeneid').text();
    var downstreamgeneid = $('#downstreamgeneid').text();

    var posIntergenic = getPosition(idintergenic);
    console.log(posIntergenic);

    var line = chart1.addFeature(new Line('gene', Math.min(posIntergenic[1], posIntergenic[2]), Math.abs(posIntergenic[2] - posIntergenic[1]), posIntergenic[0]));
    line.thickness = 20;
    line.roundness = 2;
    line.name = 'intergenic';
    line.onMouseover = 'Intergenic: ' + idintergenic;
    console.log(line.onMouseover);
    line.color = "lightgreen";
//    var geneIntergenic = chart1.addGene(posIntergenic[1], posIntergenic[2], posIntergenic[0]);
//    geneIntergenic.name = idintergenic;
//    geneIntergenic.text.color = "white";
//    geneIntergenic.roundness = 1;
//    geneIntergenic.onMouseover = idintergenic;

    if (upstreamgeneid != '') {
        var posUpstream = getPosition(upstreamgeneid);
        console.log(posUpstream);
        var geneUpstream = chart1.addGene(Math.min(posUpstream[1], posUpstream[2]), Math.abs(posUpstream[2] - posUpstream[1]), posUpstream[0]);
        geneUpstream.name = 'upstream';
        geneUpstream.text.size = '16';
        geneUpstream.roundness = 1;
        geneUpstream.onMouseover = 'Upstream Gene: ' + upstreamgeneid;
        geneUpstream.onClick = "/search/quick/?type=gene&query=" + upstreamgeneid;
    }

    if (downstreamgeneid != '') {
        var posDownstream = getPosition(downstreamgeneid);
        console.log(posDownstream);
        var geneDownstream = chart1.addGene(Math.min(posDownstream[1], posDownstream[2]), Math.abs(posDownstream[2] - posDownstream[1]), posDownstream[0]);
        geneDownstream.name = 'downstream';
        geneDownstream.text.size = "16";
        geneDownstream.roundness = 1;
        geneDownstream.onMouseover = 'Downstream Gene: ' + downstreamgeneid;
        geneDownstream.onClick = "/search/quick/?type=gene&query=" + downstreamgeneid;
    }

    // Draw Chart
    chart1.draw();

    // Create image of chart1
    var img = chart1.canvas.toDataURL("image/png");
    // Add link to download image
    document.getElementById('export').href = img;
}