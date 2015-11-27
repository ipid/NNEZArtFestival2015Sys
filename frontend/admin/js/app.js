/**
 * Written by singsong
 */

(function() {
    var loader_el = document.getElementById("loader");
    loader_el.style.display = "none";

    var container_el = document.getElementById("container");
    container_el.style.display = "";

    var mainView = $("#main_view");
    //debugger;
    mainView.children().hide();

    var previewTicketCountEl = $("#preview_ticket_count");
    function initPreview() {
        mainView.children().hide();
        $("#view_preview").show();
        Loader.show();
        // Post
        Net.queryApplicationNumber(function (e) {
            previewTicketCountEl.text(e);
            Loader.hide();
        }, function(e) {
            alert("请求失败: " + e);
            Loader.hide();
        });
    }
    $("#nav_preview").click(initPreview);

    function initTicketIndex() {
        mainView.children().hide();
        $("#view_ticket_index").show();
        Loader.show();
        loadTicketIndex();
    }
    var curIndex = 0;
    var ticketIndexTable = $("ticket_index_table");
    function loadTicketIndex() {
        Net.indexApplication(curIndex, 5, function(o) {
            if(o.state != "success") {
                alert("请求失败");
                Loader.hide();
                return;
            }

            // Remove all records
            $("#ticket_index_table tr:not(:eq(0))").remove();
            // Add new records
            var tr = document.createElement("tr");

            Loader.hide();
        }, function() {
            alert("请求失败！");
            Loader.hide();
        });
    }
    $("#nav_ticket_index").click(initTicketIndex);

    initPreview();

})();
