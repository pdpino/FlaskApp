var ARROWS = {
  keyboard_arrow_up: "keyboard_arrow_down",
  keyboard_arrow_down: "keyboard_arrow_up",
};

$(document).ready(function(){
  $(".mdl-button.mdl-button--icon.mdl-js-button.mdl-js-ripple-effect.arrow")
    .click(function() {
      var a = $(this).find("i.material-icons");
      var content = a[0].textContent;
      a.replaceWith('<i class="material-icons">'+ARROWS[content]+'</i>');
      var b = $(this).parent().parent().find(".query-card-code").toggle();
  });
  $(".mdl-button.mdl-button--icon.mdl-js-button.mdl-js-ripple-effect.play")
    .click(function() {
      var db = $(this).prev()[0].textContent.split('-')[0].trim();
      var query = $(this).parent().parent().find(".query-card-code > span")[0].textContent;
      window.location.assign(location.href+db+'?query='+query);
  });
});
