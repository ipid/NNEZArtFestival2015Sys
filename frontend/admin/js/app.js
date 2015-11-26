(function() {
    var loader_el = document.getElementById("loader");
    loader_el.style.display = "none";

    var container_el = document.getElementById("container");
    container_el.style.display = "";

    var mainView = $("#main_view");
    //debugger;
    mainView.children().hide();

    var previewTicketCountEl = $("#preview_ticket_count");
    $("#nav_preview").click(function () {
        mainView.children().hide();
        $("#view_preview").show();
        Loader.show();
        // Post
        Net.queryApplicationNumber(function (e) {
            previewTicketCountEl.text(e);
            Loader.hide();
        }, function(e) {
            alert("«Î«Û ß∞‹: " + e);
            Loader.hide();
        })
    });

    $("#nav_ticket_index").click(function () {
        mainView.children().hide();
        $("#view_ticket_index").show();
    });

})();
