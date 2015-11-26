var Net = {
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
    indexApplication: function(from, to, successFn, failed) {
        $.ajax("api/ticket/indexApplication", {
            method: "POST",
            data: {
                from: from,
                to: to
            },
            error: function() {
                if(failed) {
                    failed();
                }
            },
            success: function(res) {
                debugger;
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
        $.ajax("api/ticket/indexApplication", {
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
    deleteApplication: function(successFn, failed) {
        $.ajax("api/ticket/deleteApplication", {
            method: "POST",

        });
    }
};
