$(document).on('ready', function () {

  $(".submit_instance").on('submit', function() {
    var data = $('.add_instance').serialize()
    $.ajax({
      type: "POST",
      url: "/api/v1.0/activities/" + $(this).data("activity-id"),
      data: data,
      dataType:'json',
      success: function () {
        $("#stats").append('<td>' + "100"  + '</td>'
                    + '<td>' + data.freq + '</td>')
      }
    })
  });
});
