$(document).on('ready', function () {

  $(".view_activity").on('click', function () {
        $.ajax({
            type: "POST",
            url: "/api/v1/activity/" + $(this).data("activity.id") + "/<int:id>",
            success: function (data) {
                $("" + data['']).
                    children("").
                    after("");
                $("" + data['']).
                    find('').
                    remove();
            },
            dataType: "json"
        });
    });
