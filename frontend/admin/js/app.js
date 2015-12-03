/**
 * Written by singsong
 */

(function() {
    var REQ_FAILED = "请求失败！";

    var navigator = $("#navigator");
    $("#toolbar_nav_toggle").click(function() {
        navigator.toggleClass("navigator_show");
    });

    var mainView = $("#main_view");
    //debugger;
    mainView.children().hide();

    $("#login_verify_img").click(function() {
        this.src = /*"http://127.0.0.1:8000/" + */"api/captcha/get";
    });

    var login_pwd = $("#login_password");
    var login_verify = $("#login_verify");
    $("#login_submit").click(function() {
        Net.login(login_pwd.val(), login_verify.val(), function() {
            enterFrontEnd();
        }, function() {
            alert("登录失败");
        });
    });

    function initLogin() {
        mainView.children().hide();

        $("#view_login").show();
        Loader.hide();
    }

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
    var ticketIndexTable = document.getElementById("ticket_index_table");
    function loadTicketIndex() {
        Net.indexApplication(curIndex, 5, function(o) {
            if(o.state != "success") {
                alert("请求失败！");
                Loader.hide();
                return;
            }

            // Remove all records
            $("#ticket_index_table tr:not(:eq(0))").remove();
            // Add new records
            var result = o.result;
            for(var i=0; i<result.length; i++) {
                var tr = document.createElement("tr");
                var t_id = document.createElement("td");
                t_id.innerText = result[i]["applicationID"];
                tr.appendChild(t_id);
                var t_name = document.createElement("td");
                t_name.innerText = result[i]["name"];
                tr.appendChild(t_name);
                var t_grade = document.createElement("td");
                t_grade.innerText = result[i]["grade"];
                tr.appendChild(t_grade);
                var t_class = document.createElement("td");
                t_class.innerText = result[i]["classNo"];
                tr.appendChild(t_class);
                var t_schoolId = document.createElement("td");
                t_schoolId.innerText = result[i]["schoolID"];
                tr.appendChild(t_schoolId);
                var t_societyID = document.createElement("td");
                t_societyID.innerText = result[i]["societyID"];
                tr.appendChild(t_societyID);
                var t_requirement = document.createElement("td");
                t_requirement.innerText = result[i]["requirement"];
                tr.appendChild(t_requirement);
                ticketIndexTable.appendChild(tr);
            }
            Loader.hide();
        }, function() {
            alert("请求失败！");
            Loader.hide();
        });
    }
    $("#nav_ticket_index").click(initTicketIndex);

    function initTicketSearch() {
        mainView.children().hide();
        $("#view_ticket_search").show();
        Loader.hide();
    }
    $("#nav_ticket_filter").click(initTicketSearch);

    Net.isAdmin(enterFrontEnd, initLogin);

    function enterFrontEnd() {
        showViewport();
        initPreview();
        hideLogin();
    }

    var view_login = $("#view_login");
    function hideLogin() {
        view_login.hide();
    }

    function showViewport() {
        var container_el = document.getElementById("body");
        container_el.style.display = "";
    }

    var container_el = document.getElementById("container");
    container_el.style.display = "";

    var loader_el = document.getElementById("loader");
    loader_el.style.display = "none";



})();
