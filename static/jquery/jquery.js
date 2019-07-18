$(document).ready(function() {
  
  $('.collapsible').collapsible();
  $('select').material_select();
  $(".button-collapse").sideNav();
  Materialize.updateTextFields();
  $('.dropdown-trigger').dropdown();
  $('select').formSelect();

$(document).on("submit", "form1", function(e){
          e.preventDefault();
          alert('it works!');
          return  false;
      });    
});

/*Select cuisine on add and edit html*/

  $("body").on('click', '.duplicate_select', function() {

    var select_remove_button = ' <i class="material-icons remove_select pointer">remove</i><br>';

    if ($(this).attr('id') == 'add_cuisine') {
        $(this).prev().clone().appendTo(".cuisine_container").before(select_remove_button)
        $(this).appendTo(".cuisine_container")
        $('.duplicate_select').addClass("add-fourpx")
        $('.duplicate_select').removeClass("remove-width")
    }
  });

  $("body").on('click', '.remove_select', function() {
    $(this).prev().remove();
    $(this).next().remove();
    $(this).remove();
  });

  /*Select allergen on add and edit html*/

  $(".nuts:not(:first)").parent().remove();
  $(".dairy:not(:first)").parent().remove();
  $(".penuts:not(:first)").parent().remove();
  $(".eggs:not(:first)").parent().remove();
  $(".crustacean:not(:first)").parent().remove();
  $(".wheat:not(:first)").parent().remove();
  $(".soybeans:not(:first)").parent().remove();


  if ($('.duplicate_select').prev().prev().hasClass('remove_select')) {
    $('.duplicate_select').prev().remove()
    $('.duplicate_select').prev().remove()

  }


  /*REGISTER*/
  $('.register-close-btn').click(function() {
    $(this).parent().parent().parent().hide('fade', 500)
    $(window).off('scroll');


  $('.register-trigger').click(function() {
    $(".signin-page").hide('fade')
    $(".register-page").show('fade', 500)
    $(window).off('scroll');
    $('body,html').animate({
        scrollTop: 0
    }, 800);
    $(window).scroll(function() {
        $(window).scrollTop(current);
    });



  $('.signin-trigger').click(function() {
    $(".register-page").hide('fade')
    $(".signin-page").show('fade', 500)
    $(window).scroll(function() {
        $(window).scrollTop(current);
    });

});



