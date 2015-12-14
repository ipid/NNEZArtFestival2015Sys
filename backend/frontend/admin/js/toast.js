/**
 * Written by singsong
 */

(function() {
    var toastWrapper = $("#toast_wrapper");

    function delOneToast() {
        toastWrapper.children(":first").remove();
    }

    window.Toast = {
        make: function(msg) {
            var toast = $("<div>");
            toast.addClass("toast");
            toast.text(msg);
            toastWrapper.append(toast);
            setTimeout(delOneToast, 3000);
        }
    };
})();
