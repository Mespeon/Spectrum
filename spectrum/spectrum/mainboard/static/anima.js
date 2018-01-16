$(document).ready(function(){
  $('#data-management').hover(function(e){
    // Check if the next menu is active.
    // Remove active classes and hide  them if found.
    if ($(this).parent().next().children('li').hasClass('active')) {
      $(this).parent().next().children('li').removeClass('active');
      $('#inv-menu').slideUp(500);
    }

    $(this).addClass('active'); // Add active class to top-level menu link
    //menuTimeout = setTimeout(function(){ thisObject.delay(500).hide(); }, 2000);

    // Show the respective dropdown menu and mark it active
    $('#dtm-menu').slideDown(500, function(e){
      $(this).addClass('active');
    });
  });

  $('#inv-management').hover(function(e){
    // Check if the previous menu is active.
    // Remove active classes and hide  them if found.
    if ($(this).parent().prev().children('li').hasClass('active')) {
      $(this).parent().prev().children('li').removeClass('active');
      $('#dtm-menu').slideUp(500);
    }

    $(this).addClass('active'); // Add active class to top-level menu link

    // Show the respective dropdown menu and mark it active
    $('#inv-menu').slideDown(500, function(e){
      $(this).addClass('active');
    })
  });

  /*
  $('#navbar li').hover(function(e){
    // Get class name of top level menu item
    var className = $(this).attr('class');
    //var loc = $(this).position();
    //$('#position-jq').empty().append(className + "<br/>Top: " + loc.top + "Left: " + loc.left);

    // Conditional statements for menu appearance
    if ($(this).hasClass('data-management')) {
      // CHECK IF NEXT MENU IS ACTIVE. IF TRUE,
      // SLIDE IT UP, THEN PROCEED TO NEXT BLOCK.
      if ($('#dtm-menu').next('div').hasClass('active')){
        $('#dtm-menu').next('div').removeClass('active').fadeOut(500);
      }

      // Show the menu
      $('#dtm-menu').fadeIn(500, function(e){
        $(this).addClass('active'); // mark this menu as active

        // Execute once the mouse leaves either top level or sub menu
        $(this).mouseleave(function(e){
          $(this).fadeOut(500);
        });
      });
    }

    else if ($(this).hasClass('inv-management')) {
      // CHECK IF PREVIOUS MENU IS ACTIVE. IF TRUE,
      // SLIDE IT UP, THEN PROCEED TO NEXT BLOCK.
      if ($('#inv-menu').prev('div').hasClass('active')){
        $('#inv-menu').prev('div').removeClass('active').fadeOut(500);
      }

      // Show the menu
      $('#inv-menu').fadeIn(500, function(e){
        $(this).addClass('active'); // mark this menu as active

        // Execute if the mouse leaves the sub menu
        $(this).mouseleave(function(e){
          $(this).fadeOut(500);
        });
      });
    }

    // Execute if the mouse leaves the top menu
		$(this).mouseleave(function(e){

		});
	});
  */

  $('#wrapper').mouseenter(function (e){
    // Remove active classes from dropdown menus and hide them.
    $('#dropdown').children('.menu-container').removeClass('active').slideUp(500);
    $('.top-link').children('li').removeClass('active');
  });

  e.preventDefault();
})
