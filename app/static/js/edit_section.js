var quill, sectionText;

function htmlDecode(input){
  var e = document.createElement('div');
  e.innerHTML = input;
  return e.childNodes[0].nodeValue;
}

$(document).ready(function () {
    quill = new Quill('#snow-container', {
        placeholder: "test",
        theme: "snow"
    });
    quill.clipboard.dangerouslyPasteHTML(htmlDecode(sectionText));

    $("#section-form").on("submit", feunction () {
        var myEditor = document.querySelector("#snow-container");
        var html = myEditor.children[0].innerHTML;
        $("#text").val(html);
    });
});
