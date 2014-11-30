//detect whether support svg or canvas
//URL_PREFIX = '/ehfpi';
URL_PREFIX = '';

if (!supportSVG() && !supportCanvas()) {
    window.location.href = URL_PREFIX+'/versionUpdate/';
}

function supportSVG() {
    return document.createElement('svg').getAttributeNS
}

function supportCanvas() {
    var elem = document.createElement('canvas');
    return !!(elem.getContext && elem.getContext('2d'));
}