$(document).on('ready', function () {
  $("#log_form").submit( function(event) {
    event.preventDefault();
    $.ajax({
            type: 'post',
            url: '/api/v1/logs',
            data: $(this).serialize(),
            success: function(data) {
              alert(data);
              '<tr class="logs">'
                '<td>{{ log.item.name }}</td>' +
                '<td>{{ log.logged_at }}</td>' +
                '<td>{{ log.value }}</td>' +
                '<td><a href="/dashboard/log/edit/{{ log.id }}"><i class="fa fa-pencil-square-o editLog"></i></a></td>' +
                '<td><a href="/dashboard/log/delete/{{ log.id }}"><i class="fa fa-times"></i></a></td>' +
              '</tr>'
            },
            dataType: "json"
          });
  });
});






//   $(".logs").
//       on('mouseenter', '.editLog', function () {
//           $(this).addClass("fa-times").removeClass("fa-pencil-square-o");
//           // add click event
//       }).
//       on('mouseleave', '.editLog', function () {
//           $(this).removeClass("fa-times").addClass("fa-pencil-square-o");
//           // remove click event
//       });
// });


// submit form
// dipslay api response
// add log to list below
