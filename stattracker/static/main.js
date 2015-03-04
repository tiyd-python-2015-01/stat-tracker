$(document).on('ready', function () {
  $(".add-stat").on('click', function () {
    $.ajax({
      type: "POST",
      url: "/api/v1/books/" + $(this).data("book-id") + "/data",
      success: function (data) {
        $("#book-" + data['book_id']).
        children(".book-link").
        after(" <i class='fa fa-star favorite'></i>");
        $("#book-" + data['book_id']).
        find('.add-favorite').
        remove();
      },
      dataType: "json";
    });
  });
});
