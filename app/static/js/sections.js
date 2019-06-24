var deleteImageUrl;

$(document).ready(function() {
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
});
