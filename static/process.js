function doProcess() {
    var text = $('#igt-input').val();
    $('#instance').hide();
    $.ajax({
        url: baseUrl + 'process',
        method: 'post',
        data: {text: text},
        success: processSuccess,
        error: processError,
    });
}

function processError(jqXHR, status) {
    $('#instance').html('');
    $('#error').html(jqXHR['responseText']);
    $('#error').slideDown();
}

function processSuccess(jqXHR, status) {
    $('#error').slideUp();
    $('#instance').html(jqXHR);
    $('#instance').show();
    bindMouseEvents();
}

// Highlighting stuff

function highlightBg(arr, inclass, entering) {
    $.each(arr, function (i, o) {
        if (o.trim()) {
            var tgtSelector = '#'+o;
            var tgt = $(tgtSelector);
            if (entering) {
                tgt.addClass(inclass);
            } else
                tgt.removeClass(inclass);
        }
    });

}

function highlight(obj, entering) {
    var alntype = $(obj).attr('alntype');


    if (alntype == 'tw') {
        var posAln = $(obj).attr('posaln').split(',');
        var gAln = $(obj).attr('galn').split(',');
        highlightBg(posAln, 'pos-aln', entering);
        highlightBg(gAln, 'aln-g', entering);
    }
    else if (alntype == 'tw-pos') {
        var alnArr = $(obj).attr('aln').split(',');
        highlightBg(alnArr, 'aln-tw', entering);
    } else if (alntype == 'g' || alntype == 'gw') {
        var segment = $(obj).attr('segment').split(',');
        var tags = $(obj).attr('tags').split(',');
        var waln = $(obj).attr('waln').split(',');
        highlightBg(segment, 'segment', entering);
        highlightBg(tags, 'pos-aln', entering);
        highlightBg(waln, 'aln-g', entering);
    }

    if (alntype == 'pos') {
        var alnArr = $(obj).attr('aln').split(',');
        highlightBg(alnArr, 'aln-word', entering);
    }


}

function bindMouseEvents() {
    $('td').mouseenter(function (eo) {
        highlight(eo.target, true);
    });
    $('td').mouseleave(function (eo) {
        highlight(eo.target, false);
    });

    $('.tooltip').powerTip();
}

