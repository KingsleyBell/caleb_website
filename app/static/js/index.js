$(document).ready(function() {
  $("#home-link").click(function(e) {
    e.preventDefault();
    $(".section.active").removeClass("active");
    $(".nav-link.active").removeClass("active");
    $("#section-web-home").addClass("active");
  });

  $(".nav-link").click(function(e) {
    var targetId = e.target.id.split('-'),
    linkId = targetId[targetId.length - 1];
    $(".section.active").removeClass("active");
    $(".nav-link.active").removeClass("active");

    $("#section-" + linkId).addClass("active");
    $(this).addClass("active");
  });
});
