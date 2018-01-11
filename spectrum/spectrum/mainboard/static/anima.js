/*
$(document).ready(function(){
  $(".menu-top li").click(function(){
    $(".dropdown-menu", this).fadeIn(100);
  }, function(){
    $(".dropdown-menu", this).stop().fadeOut(100);
  });

  e.preventDefault();
});
*/

$(document).ready(function(){
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
      //className = ''; // resets the variable to an empty value

      // Fades out any active children elements of the dropdown menu div,
      // and removes the active class from them.
      //$('#dropdown').children('.menu-container').removeClass('active').delay(1000).fadeOut(500);
		});
	});

  $('body').click(function (e){
    // Remove active classes from dropdown menus and hide them.
    $('#dropdown').children('.menu-container').removeClass('active').delay(1000).fadeOut(500);
  });

  e.preventDefault();
})
