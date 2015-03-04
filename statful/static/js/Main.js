$(document).ready(function () {
    $(".stat-form").on('submit', function () {
        event.preventDefault();
        $.ajax({
            type: "POST",
            data: $(".stat-form").serializeArray(),
            url: "/api/v1/activities/" + $(this).data("activity-id") + "/stats",
            success: function (data) {
               alert($("#occurrences").val());
            },
            dataType: "json"
        });
    });

});