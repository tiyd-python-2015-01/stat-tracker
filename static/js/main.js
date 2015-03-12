$( document ).ready(function() {

  $("#stat_form").on('submit', function(event) {
    event.preventDefault();
    $.ajax({
      type: "POST",
      data: $(this).serialize(),
      url: "/api/v1/activities/" + $(this).data("a-id") + "/stats",
      success: function (data) {
      console.log(data);
       $("#thead").after(
                   '<tr><td>' + data.time  + '</td>' +
                   '<td>' + data.ammount + "<a class='button tiny radius info' href=" + data.deleteURL + '>Delete</a></td>'
                +
                 '</tr>');
       },
       dataType: "json"
    });
  });

});
