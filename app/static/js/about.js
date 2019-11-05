var quill, aboutText;

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
        placeholder: "test",
        theme: "snow"
    });
    console.log(aboutText);
    quill.clipboard.dangerouslyPasteHTML(htmlDecode(aboutText));

    $("#about-form").on("submit", function () {
        var myEditor = document.querySelector("#snow-container");
        var html = myEditor.children[0].innerHTML;
        $("#text").val(html);
    });
});
