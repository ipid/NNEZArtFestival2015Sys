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
        this.src = /*"http://127.0.0.1:8000/" + */"api/captcha/get?" + Date.now();
    });

    var login_pwd = $("#login_password");
    var login_verify = $("#login_verify");
    $("#login_submit").click(function() {
        Net.login(login_pwd.val(), login_verify.val(), function() {
            login_pwd.val(null);
            login_verify.val(null);
            enterFrontEnd();
        }, function() {
            alert("登录失败");
        });
    });

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
                alert(REQ_FAILED);
                Loader.hide();
                return;
            }
            genTicketTable(o);
            Loader.hide();
        }, function() {
            alert(REQ_FAILED);
            Loader.hide();
        });
    }
    $("#nav_ticket_index").click(initTicketIndex);

    function genTicketTable(o) {
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
            var t_control = document.createElement("td");
            t_control.innerHTML = "<a href='javascript:delTicket("+result[i].applicationID+")'>删除</a><br><a href='javascript:void(0)'>更改</a>";
            tr.appendChild(t_control);
            ticketIndexTable.appendChild(tr);
        }
    }

    function initTicketSearch() {
        mainView.children().hide();
        $("#view_ticket_search").show();
        Loader.hide();
    }
    $("#nav_ticket_filter").click(initTicketSearch);

    var ticket_search = {
        appId: $("#ticket_search_applicationID"),
        name: $("#ticket_search_name"),
        grade: $("#ticket_search_grade"),
        classNO: $("#ticket_search_class"),
        schoolID: $("#ticket_search_schoolID"),
        societyID: $("#ticket_search_societyID"),
        requirement: $("#ticket_search_require")
    };
    $("#ticket_search_submit").click(function () {
        Loader.show();
        mainView.children().hide();
        $("#view_ticket_index").show();
        Net.queryApplication({
            applicationID: ticket_search.appId.val(),
            name: ticket_search.name.val(),
            grade: ticket_search.grade.val(),
            classNO: ticket_search.classNO.val(),
            schoolID: ticket_search.schoolID.val(),
            societyID: ticket_search.societyID.val(),
            requirement: ticket_search.requirement.val()
        }, function(o) {
            if(o.state != "success") {
                alert(REQ_FAILED);
                Loader.hide();
                return;
            }
            genTicketTable(o);
            Loader.hide();
        }, function() {
            alert(REQ_FAILED);
            Loader.hide();
        });
    });

    $("#toolbar_logout").click(function () {
        Net.logout(function() {
            initLogin();
        })
    });

    function delTicket(appID) {
        Net.deleteApplication(appID, function () {
            alert("删除成功");
            initPreview();
        }, function () {
            alert(REQ_FAILED);
        });
    }
    window.delTicket = delTicket;

    /**
     * Start App
     */

    Net.isAdmin(enterFrontEnd, initLogin);

    function initLogin() {
        mainView.children().hide();
        $("#view_login").show();
        $("#body").hide();
        Loader.hide();
    }

    function enterFrontEnd() {
        showViewport();
        initPreview();
        hideLogin();
    }

    var view_login = $("#view_login");
    function hideLogin() {
        view_login.hide();
    }

    var body_el = $("#body");
    function showViewport() {
        body_el.show();
    }

    var container_el = document.getElementById("container");
    container_el.style.display = "";

    var loader_el = document.getElementById("loader");
    loader_el.style.display = "none";

})();
