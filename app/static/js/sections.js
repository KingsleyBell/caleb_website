var deleteImageUrl,
  deleteIframeUrl,
  shiftImageUrl,
  shiftSectionUrl;

$(document).ready(function() {
  $(".shift-section-down").click(function(e) {
    var targetId = e.target.id.split('-'),
    sectionId = targetId[targetId.length - 1];
    $.ajax({
      type: "POST",
      url: shiftSectionUrl,
      data: {"section_id": sectionId, "shift": 1},
      success: function(response) {
        if (response.success === true) {
          var section = $("#section-" + sectionId),
            nextSection = section.next('.card');
          $(section).before(nextSection);
        }
      }
    });
  });

  $(".shift-section-up").click(function(e) {
    var targetId = e.target.id.split('-'),
    sectionId = targetId[targetId.length - 1];
    $.ajax({
      type: "POST",
      url: shiftSectionUrl,
      data: {"section_id": sectionId, "shift": -1},
      success: function(response) {
        if (response.success === true) {
          var section = $("#section-" + sectionId),
            previousSection = section.prev('.card');
          $(section).after(previousSection);
        }
      }
    });
  });

  $(".shift-image-down").click(function(e) {
    var targetId = e.target.id.split('-'),
    sectionId = targetId[targetId.length - 2],
    imageId = targetId[targetId.length - 1];
    $.ajax({
      type: "POST",
      url: shiftImageUrl,
      data: {"section_id": sectionId, "image_id": imageId, "shift": 1},
      success: function(response) {
        if (response.success === true) {
          var image = $("#image-" + imageId),
            nextImage = image.next('.section-image');
          $(image).before(nextImage);
        }
      }
    });
  });

  $(".shift-image-up").click(function(e) {
    var targetId = e.target.id.split('-'),
    sectionId = targetId[targetId.length - 2],
    imageId = targetId[targetId.length - 1];
    $.ajax({
      type: "POST",
      url: shiftImageUrl,
      data: {"section_id": sectionId, "image_id": imageId, "shift": -1},
      success: function(response) {
        if (response.success === true) {
          var image = $("#image-" + imageId),
            previousImage = image.prev('.section-image');
          $(image).after(previousImage);
        }
      }
    });
  });

  $(".delete-section").click(function(e) {
    var targetId = e.target.id.split('-'),
    sectionId = targetId[targetId.length - 1];
    $.ajax({
      type: "POST",
      data: {"section_id": sectionId},
      success: function() {
        $("#section-" + sectionId).remove();
      }
    });
  });

  $(".delete-image").click(function(e) {
    var targetId = e.target.id.split('-'),
    sectionId = targetId[targetId.length - 2],
    imageId = targetId[targetId.length - 1];
    $.ajax({
      type: "POST",
      url: deleteImageUrl,
      data: {"image_id": imageId, "section_id": sectionId},
      success: function() {
        $("#image-" + imageId).remove();
      }
    });
  });

  $(".delete-iframe").click(function(e) {
    var targetId = e.target.id.split('-'),
    sectionId = targetId[targetId.length - 2],
    iframeId = targetId[targetId.length - 1];
    $.ajax({
      type: "POST",
      url: deleteIframeUrl,
      data: {"iframe_id": iframeId, "section_id": sectionId},
      success: function() {
        $("#iframe-" + iframeId).remove();
      }
    });
  });
});
