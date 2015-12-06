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
    queryApplicationNumber: function(successFn, failed) {
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
    indexApplication: function(from, len, successFn, failed) {
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
    queryApplication: function(data, successFn, failed) {
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
    deleteApplication: function(appID, successFn, failed) {
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
    }
};
