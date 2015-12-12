/**
 * Created by singsong on 2015/12/7.
 */

(function() {
    var ownerName = $("#ownerName");
    var ownerContact = $("#ownerContact");
    var shopName = $("#shopName");
    var ownerType = $("#ownerType");
    var ownerGrade = $("#ownerGrade");
    var ownerClass = $("#ownerClass");
    var electricity = $("#electricity");
    var food = $("#food");
    var nonFood = $("#nonfood");
    var key = $("#privilegeKey");
    var captcha = $("#captcha");

    $("#btn_submit").click(function() {

        $.ajax("/api/shop/insertApplication", {
            method: "POST",
            data: {
                ownerName: ownerName.val(),
                ownerContact: ownerContact.val(),
                shopName: shopName.val(),
                ownerType: ownerType.val(),
                ownerGrade: ownerGrade.val(),
                ownerClass: ownerClass.val(),
                electricity: electricity[0].checked ? 1 : 0,
                food: food[0].checked ? 1 : 0,
                nonFood: nonFood[0].checked ? 1 : 0,
                privilegeKey: key.val(),
                captcha: captcha.val()
            },
            error: function () {
                alert("哎呀，网络出错了");
            },
            success: function (state) {
                if(state == "error") {
                    alert("内部错误");
                }
                if(state == "illegal") {
                    alert("验证码错误");
                }
                if(state == "success")
                    alert("请求成功");
                else
                    alert("请求失败");
            }
        });
    });
})();
