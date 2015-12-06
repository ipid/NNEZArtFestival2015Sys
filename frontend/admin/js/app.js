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


    /**
     * Preview
     */
    var previewTicketCountEl = $("#preview_ticket_count");
    var previewShopCountEl = $("#preview_shop_count");
    function initPreview() {
        mainView.children().hide();
        $("#view_preview").show();
        Loader.show();
        // Post
        var responseNum = 0;
        Net.queryTicketApplicationNumber(function(num) {
            previewTicketCountEl.text(num);
            if(responseNum == 1)
                Loader.hide();
            else
                responseNum += 1;
        }, function() {
            previewTicketCountEl.text(REQ_FAILED);
            Loader.hide();
        });
        Net.queryShopApplicationNum(function(num) {
            previewShopCountEl.text(num);
            if(responseNum == 1)
                Loader.hide();
            else
                responseNum += 1;
        }, function() {
            previewShopCountEl.text(REQ_FAILED);
            Loader.hide();
        });
    }
    $("#nav_preview").click(initPreview);


    /**
     * Ticket
     */
    function initTicketIndex() {
        alert("功能未开放");
        return;
        mainView.children().hide();
        $("#view_ticket_index").show();
        Loader.show();
        loadTicketIndex();
    }
    var curTicketIndex = 0;
    var ticketIndexTable = document.getElementById("ticket_index_table");
    function loadTicketIndex() {
        Net.indexTicketApplication(curTicketIndex, 5, function(o) {
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
        alert("功能未开放");
        return;
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
        Net.queryTicketApplication({
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
        if(!confirm("你确定要删除请求" + appID + "吗？"))
            return;
        Net.deleteTicketApplication(appID, function () {
            alert("删除成功");
            initPreview();
        }, function () {
            alert(REQ_FAILED);
        });
    }
    window.delTicket = delTicket;


    /**
     * Shop
     */

    function initShopIndex() {
        mainView.children().hide();
        $("#view_shop_index").show();
        Loader.show();
        loadShopIndex();
    }
    var curShopIndex = 0;
    var shopIndexTable = document.getElementById("shop_index_table");
    function loadShopIndex() {
        Net.indexShopApplication(curShopIndex, 5, function(o) {
            if(o.state != "success") {
                alert(REQ_FAILED);
                Loader.hide();
                return;
            }
            genShopTable(o);
            Loader.hide();
        }, function() {
            alert(REQ_FAILED);
            Loader.hide();
        });
    }
    function genShopTable(o) {
        // Remove all records
        $("#shop_index_table tr:not(:eq(0))").remove();
        // Add new records
        var result = o.result;
        for(var i=0; i<result.length; i++) {
            var tr = document.createElement("tr");

            var t_id = document.createElement("td");
            t_id.innerText = result[i]["pk"];
            tr.appendChild(t_id);

            var t_owner = document.createElement("td");
            t_owner.innerText = result[i]["ownerName"];
            tr.appendChild(t_owner);

            var t_contact = document.createElement("td");
            t_contact.innerText = result[i]["ownerContact"];
            tr.appendChild(t_contact);

            var t_shopName = document.createElement("td");
            t_shopName.innerText = result[i]["shopName"];
            tr.appendChild(t_shopName);

            var t_ownerType = document.createElement("td");
            t_ownerType.innerText = result[i]["ownerType"];
            tr.appendChild(t_ownerType);

            var t_grade = document.createElement("td");
            t_grade.innerText = result[i]["ownerGrade"];
            tr.appendChild(t_grade);

            var t_class = document.createElement("td");
            t_class.innerText = result[i]["ownerClass"];
            tr.appendChild(t_class);

            var t_useElectricity = document.createElement("td");
            t_useElectricity.innerText = result[i]["electricity"];
            tr.appendChild(t_useElectricity);

            var t_isFood = document.createElement("td");
            t_isFood.innerText = result[i]["food"];
            tr.appendChild(t_isFood);

            var t_nonFood = document.createElement("td");
            t_nonFood.innerText = result[i]["nonFood"];
            tr.appendChild(t_nonFood);

            var t_key = document.createElement("td");
            t_key.innerText = result[i]["privilegeKey"];
            tr.appendChild(t_key);


            var t_control = document.createElement("td");
            t_control.innerHTML = "<a href='javascript:delShop(" + result[i]["pk"] + ")'>删除</a><br><a href='javascript:void(0)'>更改</a>";
            tr.appendChild(t_control);
            shopIndexTable.appendChild(tr);
        }
    }
    $("#nav_shop_index").click(initShopIndex);

    function delShop(appID) {
        if(!confirm("你确定要删除请求" + appID + "吗？"))
            return;
        Net.deleteShopApplication(appID, function () {
            alert("删除成功");
            initPreview();
        }, function () {
            alert(REQ_FAILED);
        });
    }
    window.delShop = delShop;


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
