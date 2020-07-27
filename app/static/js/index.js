$(document).ready(function() {
  $("#home-link").click(function(e) {
    e.preventDefault();
    $(".section.active").removeClass("active");
    $(".nav-link.active").removeClass("active");
    $("#section-web-home").addClass("active");
  });

  $(".nav-link").click(function(e) {
    var targetId = e.target.id.split("-"),
    linkId = targetId[targetId.length - 1];
    $(".section.active").removeClass("active");
    $(".nav-link.active").removeClass("active");

    $("#section-" + linkId).addClass("active");
    $(this).addClass("active");
  });

  $(".menu-nav").click(function(e) {
    var targetId = e.target.href.split("-"),
      linkId = targetId[targetId.length - 1];
    $("#section-" + linkId + " .menu-nav.active.show").removeClass("active show");
  });

  $(".section-expand").click(function(e) {
    let item = $(this).children("span:first");
    invertCollapse(item);
  });

  function invertCollapse(item) {
    if (item.html() == "+") {
      item.html("-")
    }
    else {
      item.html("+")
    }
  }
});
