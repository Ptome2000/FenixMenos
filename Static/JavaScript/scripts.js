$(document).ready(function() {

  // Community Scripts

  $(".group-header ").click(function() {
    let element = $(this).next();
    element.fadeToggle(500);
  })

  $('#togglePostOptions').click(function() {
    $('#PostOptions').toggle();
  });

  //

});

