$(document).ready(() => {

  // Click on the "Sign in" button
  $('#open-login-form').click(e => {
    revealPopupWrapper();
    $('#login-window').addClass('popup-window-revealed');

    $('#login-window').css({
      'transform': 'translateY(0)'
    });
  });


  // Click on the close button in the popup window
  $('.popup-close').click(e => {
    $('#login-wrapper').css({
      'visibility': 'hidden',
      'opacity': 0
    });

    $('#login-window').css({
      'transform': 'translateY(40px)'
    });

    $('#login-window').removeClass('popup-window-revealed');

    setTimeout(() => {
      $('#login-window').css({
        'transform': 'translateY(-40px)'
      });
    }, 400);
  });

  // Click on the sign up button
  $('#open-register-window').click(e => {
    revealPopupWrapper();
    $('#popup-registerbtns').addClass('popup-registerbtns-revealed');
  });

  // Click on the close button in the registration popup window
  $('#popup-registerbtns .popup-close').click(e => {
    hidePopupWrapper();
    $('#popup-registerbtns').removeClass('popup-registerbtns-revealed');

    $('#popup-registerbtns').addClass('popup-registerbtns-gone');

    setTimeout(() => {
      $('#popup-registerbtns').removeClass('popup-registerbtns-gone');
    }, 400);
  });

  // For register pages
  $('.register-page').removeClass('register-page-hidden');

  // Profile links block in the header panel
  $('#header-panel-profile-btn').click(e => {
    $('#header-panel-profile-links').toggleClass('header-panel-profile-links-visible');
  });

  // Click on whatever place except for button in the header panel will hide profile links
  $(document).click(e => {
    console.log('im here')
    console.log($('#header-panel-profile-links').is($(e.target).closest('#header-panel-profile-links')))

    if ($(e.target).is($('#header-panel-profile-btn'))) {
      e.stopPropagation();
      return;
    }

    if ($('#header-panel-profile-links').is($(e.target).closest('#header-panel-profile-links'))) {
      e.stopPropagation();
      return;
    }

    $('#header-panel-profile-links').removeClass('header-panel-profile-links-visible');
  });

  // University profile page
  $('.page-university-header').removeClass('page-university-header-hidden');

  setTimeout(() => {
    $('.page-university-ownertools').removeClass('page-university-ownertools-hidden');
    $('.page-university-info').removeClass('page-university-info-hidden');
  }, 150);

  setTimeout(() => {
    $('.page-university-programs').removeClass('page-university-programs-hidden');
  }, 400);

  // Click on hello block close button
  $('#hello-close svg').click(e => {
    let helloBlock = $(e.target).closest('.hello-block');

    $(helloBlock).css({
      'opacity': 0
    });

    setTimeout(() => {
      let height = $(helloBlock).outerHeight();
      $(helloBlock).css({'height': height + 'px'});

      $(helloBlock).css({
        'height': 0,
        'margin': 0,
        'padding': 0
      });



      setTimeout(() => {
        $(helloBlock).remove();
      }, 400);
    }, 400);
  });
});
