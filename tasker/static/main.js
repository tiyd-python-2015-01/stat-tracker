$(document).on('ready', function () {
        $("#add_stat_form").on('submit', function() {
        var data = $("#add_stat_form").serialize();
        alert(data);
        alert("/api/v1/activities/" + $(this).data("task-id") + "/stats");
        $.ajax({
            type: "POST",
            url: "/api/v1/activities/" + $(this).data("task-id") + "/stats",
            data: data,
            success: function (data) {
              alert('hello');
              // $(".stat_rows").children("<tr class='stat_row'><td <strong>"+
              //                        "data['date']:</strong></td>"+
              //                        "<td>  data['value']</td> </tr>");
                                     }, //success
            dataType: "json"
          }); //ajax
           });//add_stat_click
}); //document
