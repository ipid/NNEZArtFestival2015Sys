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

    /**
     * App control
     */

    $("#login_verify_img").click(function() {
        this.src = /*"http://127.0.0.1:8000/" + */"/api/captcha/get?" + Date.now();
    });

    var login_pwd = $("#login_password");
    var login_verify = $("#login_verify");
    $("#login_submit").click(function() {
        Loader.show();
        Net.login(login_pwd.val(), login_verify.val(), function() {
            login_pwd.val(null);
            login_verify.val(null);
            enterFrontEnd();
            Loader.hide();
        }, function() {
            alert("登录失败");
            Loader.hide();
        });
    });

    $("#toolbar_logout").click(function() {
        if(!confirm("您确定要登出吗？"))
            return;
        Loader.show();
        Net.logout(function() {
            initLogin();
            Loader.hide();
        }, function() {
            alert(REQ_FAILED);
            Loader.hide();
        });
    });


    /**
     * Preview
     */
    var previewTicketCountEl = $("#preview_ticket_count");
    var previewShopCountEl = $("#preview_shop_count");
    var FETCHING = "正在获取";

    function initPreview() {
        previewTicketCountEl.text(FETCHING);
        previewShopCountEl.text(FETCHING);
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
        //alert("功能未开放");
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
        for(var i = 0; i < result.length; i++) {
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
            t_control.innerHTML = "<a href='javascript:delTicket(" + result[i].applicationID + ")'>删除</a><br><a href='javascript:void(0)'>更改</a>";
            tr.appendChild(t_control);
            ticketIndexTable.appendChild(tr);
        }
    }

    function initTicketSearch() {
        //alert("功能未开放");
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
    $("#ticket_search_submit").click(function() {
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

    function delTicket(appID) {
        if(!confirm("你确定要删除请求" + appID + "吗？"))
            return;
        Net.deleteTicketApplication(appID, function() {
            alert("删除成功");
            initPreview();
        }, function() {
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
    var itemsPerPage = 20;
    var shopIndexTable = document.getElementById("shop_index_table");

    function loadShopIndex() {
        Net.indexShopApplication(curShopIndex, itemsPerPage, function(o) {
            if(o.state != "success") {
                alert(REQ_FAILED);
                Loader.hide();
                return;
            }
            genShopTable(o, true);
            Loader.hide();
        }, function() {
            alert(REQ_FAILED);
            Loader.hide();
        });
    }

    var shopPrePage = $("#shop_index_prePage");
    var shopNextPage = $("#shop_index_nextPage");
    shopPrePage.click(function() {
        curShopIndex -= itemsPerPage;
        if(curShopIndex < 0)
            curShopIndex = 0;
        initShopIndex();
    });
    shopNextPage.click(function() {
        curShopIndex += itemsPerPage;
        initShopIndex();
    });

    var ownerTypes = ["凤岭高中部班级/国际班", "教师", "凤岭高中部社团/国际班社团", "凤岭高中部个人/国际班个人", "非学生个人", "东盟中学", "二中初中部/新民中学"];

    function getOwnerTypeString(type) {
        var r = ownerTypes[type];
        if(r == undefined)
            return "未知代号" + type;
        return r;
    }

    function getElectricityState(num) {
        if(num == "1")
            return "用电";
        if(num == "0")
            return "不用电";
        return "！非法输入！";
    }

    function getFoodState(num) {
        if(num == "1")
            return "有食物";
        if(num == "0")
            return "没有食物";
        return "！非法输入！";
    }

    function getNonFoodState(num) {
        if(num == "1")
            return "有非食物";
        if(num == "0")
            return "没有非食物";
        return "！非法输入！";
    }

    function getClassStr(num) {
        if(num == "51")
            return "A1";
        if(num == "52")
            return "A2";
        if(num == "53")
            return "A3";
        if(num == "54")
            return "A4";
        return num;
    }

    function genShopTable(o, showBtns) {
        // Remove all records
        $("#shop_index_table tr:not(:eq(0))").remove();
        // Add new records
        var result = o.result;
        for(var i = 0; i < result.length; i++) {
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
            t_ownerType.innerText = getOwnerTypeString(result[i]["ownerType"]);
            tr.appendChild(t_ownerType);

            var t_grade = document.createElement("td");
            t_grade.innerText = result[i]["ownerGrade"];
            tr.appendChild(t_grade);

            var t_class = document.createElement("td");
            t_class.innerText = getClassStr(result[i]["ownerClass"]);
            tr.appendChild(t_class);

            var t_useElectricity = document.createElement("td");
            t_useElectricity.innerText = getElectricityState(result[i]["electricity"]);
            tr.appendChild(t_useElectricity);

            var t_isFood = document.createElement("td");
            t_isFood.innerText = getFoodState(result[i]["food"]);
            tr.appendChild(t_isFood);

            var t_nonFood = document.createElement("td");
            t_nonFood.innerText = getNonFoodState(result[i]["nonFood"]);
            tr.appendChild(t_nonFood);

            var t_key = document.createElement("td");
            t_key.innerText = result[i]["privilegeKey"];
            tr.appendChild(t_key);

            var t_control = document.createElement("td");
            t_control.innerHTML = "<a href='javascript:delShop(" + result[i]["pk"] + ")'>删除</a><br><a href='javascript:initShopUpdate(" + result[i]["pk"] + ")'>更改</a>";
            tr.appendChild(t_control);
            shopIndexTable.appendChild(tr);
        }
        shopPrePage.hide();
        shopNextPage.hide();
        if(showBtns) {
            if(curShopIndex > 0)
                shopPrePage.show();
            if(result.length >= itemsPerPage)
                shopNextPage.show();
        }
    }

    $("#nav_shop_index").click(initShopIndex);

    function delShop(appID) {
        if(!confirm("你确定要删除请求" + appID + "吗？"))
            return;
        Net.deleteShopApplication(appID, function() {
            alert("删除成功");
            initShopIndex();
        }, function() {
            alert(REQ_FAILED);
        });
    }

    window.delShop = delShop;

    function initShopSearch() {
        mainView.children().hide();
        $("#view_shop_search").show();
        Loader.hide();
    }

    $("#nav_shop_filter").click(initShopSearch);

    var shop_search = {
        appID: $("#shop_search_applicationID"),
        ownerName: $("#shop_search_ownerName"),
        contact: $("#shop_search_contact"),
        shopName: $("#shop_search_shopName"),
        ownerType: $("#shop_search_ownerType"),
        grade: $("#shop_search_grade"),
        classNO: $("#shop_search_class"),
        useElectricity: $("#shop_search_electricity"),
        food: $("#shop_search_hasFood"),
        nonFood: $("#shop_search_hasNonFood"),
        key: $("#shop_search_key")
    };
    $("#shop_search_submit").click(function() {
        Loader.show();
        mainView.children().hide();
        $("#view_shop_index").show();
        Net.queryShopApplication({
            pk: shop_search.appID.val(),
            ownerName: shop_search.ownerName.val(),
            ownerContact: shop_search.contact.val(),
            shopName: shop_search.shopName.val(),
            ownerType: shop_search.ownerType.val(),
            ownerGrade: shop_search.grade.val(),
            ownerClass: shop_search.classNO.val(),
            electricity: shop_search.useElectricity.val(),
            food: shop_search.food.val(),
            nonFood: shop_search.nonFood.val(),
            privilegeKey: shop_search.key.val()
        }, function(o) {
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
    });

    var shop_update = {
        appID: $("#shop_update_applicationID"),
        ownerName: $("#shop_update_ownerName"),
        contact: $("#shop_update_contact"),
        shopName: $("#shop_update_shopName"),
        ownerType: $("#shop_update_ownerType"),
        grade: $("#shop_update_grade"),
        classNO: $("#shop_update_class"),
        useElectricity: $("#shop_update_electricity"),
        food: $("#shop_update_hasFood"),
        nonFood: $("#shop_update_hasNonFood"),
        key: $("#shop_update_key")
    };

    function initShopUpdate(appID) {
        mainView.children().hide();
        $("#view_shop_update").show();
        Loader.show();
        Net.queryShopApplication({
            pk: appID,
            ownerName: "",
            ownerContact: "",
            shopName: "",
            ownerType: "",
            ownerGrade: "",
            ownerClass: "",
            electricity: "",
            food: "",
            nonFood: "",
            privilegeKey: ""
        }, function(o) {
            //debugger;
            if(o.result.length != 1) {
                alert("请求错误");
                return;
            }
            var re = o.result[0];
            shop_update.appID.val(re.pk);
            shop_update.ownerName.val(re.ownerName);
            shop_update.contact.val(re.ownerContact);
            shop_update.shopName.val(re.shopName);
            shop_update.ownerType.val(re.ownerType);
            shop_update.grade.val(re.ownerGrade);
            shop_update.classNO.val(re.ownerClass);
            shop_update.useElectricity.val(re.electricity);
            shop_update.food.val(re.food);
            shop_update.nonFood.val(re.nonFood);
            shop_update.key.val(re.privilegeKey);
            Loader.hide();
        }, function() {
            alert(REQ_FAILED);
            Loader.hide();
        });
    }

    window.initShopUpdate = initShopUpdate;
    $("#shop_update_submit").click(function() {
        Loader.show();
        Net.updateShopApplication({
            pk: shop_update.appID.val(),
            ownerName: shop_update.ownerName.val(),
            ownerContact: shop_update.contact.val(),
            shopName: shop_update.shopName.val(),
            ownerType: shop_update.ownerType.val(),
            ownerGrade: shop_update.grade.val(),
            ownerClass: shop_update.classNO.val(),
            electricity: shop_update.useElectricity.val(),
            food: shop_update.food.val(),
            nonFood: shop_update.nonFood.val(),
            privilegeKey: shop_update.key.val()
        }, function() {
            alert("请求成功");
            initPreview();
            Loader.hide();
        }, function() {
            alert(REQ_FAILED);
            Loader.hide();
        });
    });


    /**
     * About
     */

    function initAbout() {
        mainView.children().hide();
        $("#view_about").show();
    }
    $("#nav_about").click(initAbout);


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
