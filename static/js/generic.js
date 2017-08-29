$(document).ready(function() {	
  
  $('input[placeholder], textarea[placeholder]').placeholder();
	
});

$(function() {

	$('a, span').not('[class^=ui-]').tooltip({
		position: {
			my: "center bottom-5",
			at: "center top",
			using: function( position, feedback ) {
				$( this ).css( position );
				$( "<div>" )
				.addClass( "arrow" )
				.addClass( feedback.vertical )
				.addClass( feedback.horizontal )
				.appendTo( this );
			}
		}
	});
  
  $('body').on('click', function (e) {
    if ($(e.target).closest(".select.open").length === 0) {
      $(".select.open").find(".values-list").css({ height: '0', visibility: 'hidden' });
      $(".select.open").removeClass('open')
    }
    if ($(e.target).closest(".breadcrumbs-layer, .breadcrumbs-item a.no-underline").length === 0) {
      $('.breadcrumbs-layer').hide();
    }
    if ($(e.target).closest(".search-layer, .search-switch a").length === 0) {
      $('.search-layer').hide();
    }
  });
  
  $('.breadcrumbs-item a.no-underline').bind('click', function(event){
    event.preventDefault();
    $('.breadcrumbs-layer').hide();
    $(this).next().show();
  });
  
  $('.search-switch a').bind('click', function(event){
    event.preventDefault();
    $(this).next().show();
  })
  
  /** Закрытие слоя **/
  $('.layer-close, .shadow-layer').bind('click', function(event){
    event.preventDefault();
    $('.layer, .shadow-layer').hide();
  });
  
  /** Показывает слой с id указанным в аттрибуте data-show **/
  $('a[data-show], span[data-show], button[data-show], input[data-show], div[data-show]').each(function(){
      $(this).click(function(event){
          event.preventDefault();
          $('.layer').hide();
          layer   = $('#'+$(this).attr('data-show'));
          layer.css('margin-left', -1*layer.width()/2);
          layer.css('margin-top', -1*layer.height()/2);
          layer.css('top', $(window).scrollTop() + $(window).height()/2);
          layer.show();
          $('.shadow-layer').show();
      });
  });
  
  /** открытие/закрытие **/  
  $('.toggle-link').bind('click', function(event) {
    event.preventDefault();
    $(this).toggleClass('active');
    $(this).next('.toggle-container').slideToggle();
  })
  

  $(".carousel-button-right").on('click',function(){ 
    var carusel = $(this).parents('.carousel');
    right_carusel(carusel);
  });
  $(".carousel-button-left").on('click',function(){ 
    var carusel = $(this).parents('.carousel');
    left_carusel(carusel);
  });
  function left_carusel(carusel){
     var block_width = $(carusel).find('.carousel-block').width() + 0;
     $(carusel).find(".carousel-items .carousel-block").eq(-1).clone().prependTo($(carusel).find(".carousel-items tr")); 
     $(carusel).find(".carousel-items").css({"left":"-"+block_width+"px"}); 
     $(carusel).find(".carousel-items").animate({left: "0px"}, 200); 
     $(carusel).find(".carousel-items .carousel-block").eq(-1).remove(); 
  }
  function right_carusel(carusel){
     var block_width = $(carusel).find('.carousel-block').width() + 0;
     $(carusel).find(".carousel-items").animate({left: "-"+ block_width +"px"}, 200); 
     setTimeout(function () { 
        $(carusel).find(".carousel-items .carousel-block").eq(0).clone().appendTo($(carusel).find(".carousel-items tr")); 
        $(carusel).find(".carousel-items .carousel-block").eq(0).remove(); 
        $(carusel).find(".carousel-items").css({"left":"0px"}); 
     }, 300);
  };
  
  $('.main-menu li').hover(function(){
    $(this).addClass('active');
    var $this = $(this),
        $menu = $('.main-menu'),
        $popup = $(this).find('.menu-popup');
    $popup.css('left', 0);
    if ( $popup.hasClass('column1-full') ) {
      $popup.css('left', 0);
    } else {
      if ( $popup.hasClass('column1') || $popup.hasClass('column2') ) {
        if ( parseInt($menu.width()) < (parseInt($popup.width()) + $this.offset().left - $('.main-menu').offset().left) ) {
          $popup.css({'left':'auto','right':0});
        } else {
          $popup.css('left',$this.offset().left - $('.main-menu').offset().left);
        }
      }
    }
    $popup.show();
  },function(){
    $(this).removeClass('active');
    $(this).find('.menu-popup').hide();
  });
  
  $('.layer-link').click(function(){
    $('.for-quick-tour').slideToggle(600);
  });
  
  
  var main_menu_pos = parseInt($('.header-logo').offset().left - $('.header .main-menu li:first-child .in').offset().left);
  $('.header .main-menu-wrap').css('left',main_menu_pos);
  if ( main_menu_pos > 0 ) {
    $('.header .main-menu-wrap').css('width',$(this).find('.main-menu').width() - 2*main_menu_pos);
  };
  
  var menu_popup_padd = parseInt($('.main-menu li:first-child .in').offset().left - $('.main-menu li:first-child .in').parent().offset().left);
  $('.menu-popup').css('padding-left',menu_popup_padd + 'px');
  
  
  $('.main-menu-all').click(function(){
    $('.main-menu').hasClass('main-menu-open') ? $('.main-menu').removeClass('main-menu-open') : $('.main-menu').addClass('main-menu-open');
  })
});