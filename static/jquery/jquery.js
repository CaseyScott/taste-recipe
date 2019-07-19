$(document).ready(function() {
  
  $('select').material_select();
  Materialize.updateTextFields();
  $(".button-collapse").sideNav();
  $('.dropdown-trigger').dropdown();
  $('select').formSelect();
  $('textarea-description').val('New Text');
  $('textarea-description').trigger('autoresize');
  $('textarea-ingredients').val('New Text');
  $('textarea-ingredients').trigger('autoresize');
  $('textarea-instructions').val('New Text');
  $('textarea-instructions').trigger('autoresize');
});









