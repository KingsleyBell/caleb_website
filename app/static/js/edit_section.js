var quill, sectionText;

function htmlDecode(input){
  if (input.length == 0) {
    return input;
  }
  var e = document.createElement('div');
  e.innerHTML = input;
  return e.childNodes[0].nodeValue;
}

$(document).ready(function () {
    quill = new Quill('#snow-container', {
        placeholder: "Section text here",
        theme: "snow"
    });
    quill.clipboard.dangerouslyPasteHTML(htmlDecode(sectionText));

    $("#section-form").on("submit", function (e) {
        if (quill.getLength() <=  1) {
          $("#text").val("");
        }
        else {
          var myEditor = document.querySelector("#snow-container");
          var html = myEditor.children[0].innerHTML;
          $("#text").val(html);
        }
    });
});
