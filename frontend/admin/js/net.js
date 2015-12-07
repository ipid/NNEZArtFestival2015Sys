var Net = {
    login: function(pwd, ver, successFn, failed) {
        $.ajax("api/admin/login", {
            method: "POST",
            data: {
                password: pwd,
                captcha: ver
            },
            error: function() {
                failed();
            },
            success: function(re) {
                if(re != "success")
                    failed();
                else
                    successFn();
            }
        });
    },
    logout: function(successFn, failed) {
        $.ajax("api/admin/logout", {
            method: "POST",
            error: function () {
                failed();
            },
            success: function(state) {
                if(state != "success")
                    failed();
                else
                    successFn();
            }
        });
    },
    isAdmin: function(successFn, failed) {
        $.ajax("api/admin/isAdmin", {
            method: "POST",
            error: function() {
                failed();
            },
            success: function(code) {
                if(code == "1")
                    successFn();
                else
                    failed();
            }
        });
    },

    /**
     * Ticket
     */
    queryTicketApplicationNumber: function(successFn, failed) {
        $.ajax("api/ticket/queryApplicationNumber", {
            method: "POST",
            error: function() {
                if(failed)
                    failed("error");
            },
            success: function(response) {
                if(response == "failure") {
                    if(failed) {
                        failed("failure");
                    }
                }else{
                    if(successFn) {
                        successFn(response);
                    }
                }
            }
        });
    },
    indexTicketApplication: function(from, len, successFn, failed) {
        $.ajax("api/ticket/indexApplication", {
            method: "POST",
            data: {
                from: from,
                len: len
            },
            error: function() {
                if(failed) {
                    failed();
                }
            },
            success: function(res) {
                var o = JSON.parse(res);
                if(o.state != "success") {
                    failed(o.state);
                }else{
                    successFn(o);
                }
            }
        });
    },
    queryTicketApplication: function(data, successFn, failed) {
        $.ajax("api/ticket/queryApplication", {
            method: "POST",
            data: data,
            error: function() {
                if(failed) {
                    failed();
                }
            },
            success: function(e) {
                var o = JSON.parse(e);
                if(o.state != "success") {
                    failed(o.state);
                }else{
                    successFn(o);
                }
            }
        });
    },
    deleteTicketApplication: function(appID, successFn, failed) {
        $.ajax("api/ticket/deleteApplication", {
            method: "POST",
            data: {
                applicationID: appID
            },
            error: function() {
                failed();
            },
            success: function(state) {
                if(state != "success")
                    failed();
                else
                    successFn();
            }
        });
    },

    /**
     * Shop
     */
    queryShopApplicationNum: function(successFn, failed) {
        $.ajax("api/shop/queryApplicationNumber", {
            method: "POST",
            error: function() {
                failed();
            },
            success: function(num) {
                successFn(num);
            }
        });
    },
    indexShopApplication: function(from, len, successFn, failed) {
        $.ajax("api/shop/indexApplication", {
            method: "POST",
            data: {
                from: from,
                len: len
            },
            error: function() {
                failed();
            },
            success: function(objStr) {
                var o = JSON.parse(objStr);
                if(o.state != "success")
                    failed();
                else
                    successFn(o);
            }
        });
    },
    deleteShopApplication: function(appID, successFn, failed) {
        $.ajax("api/shop/deleteApplication", {
            method: "POST",
            data: {
                pk: appID
            },
            error: function() {
                failed();
            },
            success: function(state) {
                if(state != "success")
                    failed();
                else
                    successFn();
            }
        });
    },
    queryShopApplication: function(data, successFn, failed) {
        $.ajax("api/shop/queryApplication", {
            method: "POST",
            data: data,
            error: function() {
                failed();
            },
            success: function(objStr) {
                var o = JSON.parse(objStr);
                if(o.state != "success")
                    failed();
                else
                    successFn(o);
            }
        });
    },
    updateShopApplication: function(data, successFn, failed) {
        $.ajax("api/shop/modifyApplication", {
            method: "POST",
            data: data,
            error: function() {
                failed();
            },
            success: function(state) {
                if(state != "success")
                    failed();
                else
                    successFn();
            }
        });
    }
};
