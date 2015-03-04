$(document).on('ready', function () {
        $("#add_stat_form").on('submit', function() {
        alert($(this).serialize());
        alert("/tasker/api/v1/stats/" + $(this).data("task-id") + "/data");
        $.ajax({
            url: "/tasker/api/v1/stats/" + $(this).data("task-id") + "/data",
            type: "POST",
            data: data,
            success: function (data) {
              alert('hello');
              // $(".stat_rows").append("<tr class='stat_row'><td <strong>"+
              //                        "data['date']:</strong></td>"+
              //                        "<td>  data['value']</td> </tr>");
                                     }, //success
            dataType: "json",
          }); //ajax
        });//add_stat_form
}); //document
