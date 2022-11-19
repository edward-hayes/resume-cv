var coll = document.getElementsByClassName("collapsible");
var i;

for (i = 0; i < coll.length; i++) {
  coll[i].addEventListener("click", function() {
    this.classList.toggle("active");
    var content = this.nextElementSibling;
    if (!content.style.display) {
      content.style.display = getComputedStyle(content).display;
    }
    if (content.style.display === "block") {
      content.style.display = "none";
    } else {
      content.style.display = "block";
    }
  });
}

$(function(){
  $('img.image').each(function(e){
    var src = $(this).attr('src');
    $(this).hover(function(){
      $(this).attr('src', src.replace('.png', '.gif'));
    }, function(){
      $(this).attr('src', src);
    });
  });
});