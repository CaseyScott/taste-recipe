$(document).ready(function () {

 /*REGISTER*/
 $('.register-close-btn').click(function() {
  $(this).parent().parent().parent().hide('fade', 500)
  $(window).off('scroll');
});

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

});

$('.signin-trigger').click(function() {
  $(".register-page").hide('fade')
  $(".signin-page").show('fade', 500)
  $(window).scroll(function() {
      $(window).scrollTop(current);
  });

});
})
