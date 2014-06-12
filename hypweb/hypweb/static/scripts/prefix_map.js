SELECTED_SHIFT = 2

function resetSelectedPrefix() {
    var selected = $("#prefixMap .selected");
    if (selected.length > 0) {
        var pos = selected.position();
        selected.css("top", pos.top + SELECTED_SHIFT);
        selected.css("left", pos.left + SELECTED_SHIFT);
        selected.removeClass("selected");
        $("#prefixProperties .property").html("");
        $("#prefixProperties .property").eq(0).html("<em>None selected</em>");
    }
}

function selectPrefix(prefixId) {
    resetSelectedPrefix();

    var selected = $("#prefixMap .prefix[prefixId='" + prefixId + "']");
    var pos = selected.position();
    selected.css("top", pos.top - SELECTED_SHIFT);
    selected.css("left", pos.left - SELECTED_SHIFT);
    selected.addClass("selected");
    selected.appendTo("#prefixMap");
    
    var infoSrc = $("#prefixList *[prefixId='" + prefixId + "'] .property");
    var infoDst = $("#prefixProperties .property");
    for (var i = 0; i < infoSrc.length; i++) {
        infoDst.eq(i).text(infoSrc.eq(i).text());
    }
}

function prefixMapInit() {
    if ($("#prefixMap").length > 0) {
        $("*[prefixId]").hover(
            function () {
                selectPrefix($(this).attr("prefixId"));
            },
            function () {
                resetSelectedPrefix();
            }
        );
    }
}
