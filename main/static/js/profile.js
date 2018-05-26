$(document).ready(() => {
  $('#page-studentprofile').removeClass('page-studentprofile-hidden');

  $('.studentprofile-nav ul li span').click(e => {
    let clicked = e.target;
    let clickedLi = $(clicked).closest('li');
    let currentActive = $('.studentprofile-nav ul li span.active');
    let currentActiveLi = $('.studentprofile-nav ul li span.active').closest('li');
    let newHeader = $(clicked).html();
    let currentActiveNum;
    let newActiveNum;
    let i = 0;

    let listItems = $('.studentprofile-nav ul li');

    for (li of listItems) {

      if (clickedLi.is(li)) {
        newActiveNum = i;
      }

      if (currentActiveLi.is(li)) {
        currentActiveNum = i;
      }

      i++;
    }

    $(currentActive).removeClass('active');
    $(clicked).addClass('active');

    $('.studentprofile-body-content > div:nth-child(' + (currentActiveNum + 1) + ')').addClass('studentprofile-div-hidden');
    $('.studentprofile-body-content > div:nth-child(' + (newActiveNum + 1) + ')').removeClass('studentprofile-div-hidden');
    $('#studentprofile-body-top-title').html(newHeader);
  });
});
