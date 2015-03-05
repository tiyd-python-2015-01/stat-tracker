$(document).on('ready', function () {

  $(".submit_instance").on('submit', function() {
    var data = $( this ).serialize()
    $.ajax({
      type: "POST",
      url: "/api/v1.0/activities/" + $('.add_instance').data("activity-id") +"/instance",
      data: data,
      dataType:'json',
      success: function () {
        $("#stats").append('<td>' + data.date  + '</td>'
                    + '<td>' + data.freq + '</td>')
      }
    })
  });
});
