$(document).on('ready', function () {

  $(".submit_instance").on('submit', function() {
    var datas = $(".submit_instance")
    console.log(datas)
    $.ajax({
      type: "POST",
      data: JSON.stringify(datas),
      url: "/api/v1.0/activities/" + $('.submit_instance').data("activity-id") +"/instance",
      dataType:'json',
      success: function () {
        $("#stats").append('<td>' + data.date  + '</td>'
                    + '<td>' + data.freq + '</td>')
      }
    })
  });
});
