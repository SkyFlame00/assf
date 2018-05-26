function recountHiddenInputs() {
  //<input type="hidden" value="${value}" name="form-${number}-competencies" id="id_form-${number}-competencies" />
  let pillsAmount = $('.competency-pill').length;

  if (pillsAmount != 0) {
    for (let i = 0; i < pillsAmount; i++) {

      let expression = 2 * i + 1;
      console.log($(`#competencies input:nth-child(${expression})`));
      $(`#competencies input:nth-child(${expression})`).attr({
        name: `form-${i}-competencies`,
        id: `id_form-${i}-competencies`
      });
      //$('.competency-pill').children(i).prev().attr('name', `form-${i}-competencies`);
      //$('.competency-pill').children(i).prev().attr('id', `id_form-${i}-competencies`);
    }
  }
}

$(document).ready(() => {
  


  // For competencies adding
  // Remove initial hidden input for competency pill because it is not needed
  $('input[name="competency-0-competency"]').remove();
  $('input[name="competency-TOTAL_FORMS"]').val(0);

  // When clicked on option at subject area select
  $('#subject-areas').change(e => {
    let subjectAreaId = parseInt($(e.target).find('option:selected').val());

    data = {'subject_area_id': subjectAreaId};

    $.ajax({
      url: '/get-subjectarea/',
      data: data,
      success: result => {
        result = JSON.parse(result);
        let competencies = [];

        for (let key of Object.keys(result)) {
          competencies.push(result[key]);
        }

        // Remove all the options existed from the select at the moment of clicking
        $('#competencies-select option').remove();
        $('#competencies-select').append(`<option></option>`);
        for (let i = 0; i < competencies.length; i++) {
          $('#competencies-select').append(`<option value="${competencies[i].id}">${competencies[i].title}</option>`);
        }
      }
    });

  });

  $('#competencies-select').change(e => {
    let selected = $(e.target).find('option:selected');
    let value = $(e.target).find('option:selected').val();
    let title = $(e.target).find('option:selected').html();
    $('#competencies-select option:first-child').attr('selected','selected');
    $('#competencies-select option:first-child').removeAttr('selected');
    let inputsAmount = $('input[name="competency-TOTAL_FORMS"]').val();
    $('input[name="competency-TOTAL_FORMS"]').val(++inputsAmount);

    // First add a pill into a special competencies block
    const svg = `<svg version="1.1" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 21.9 21.9" xmlns:xlink="http://www.w3.org/1999/xlink" enable-background="new 0 0 21.9 21.9">
      <path d="M14.1,11.3c-0.2-0.2-0.2-0.5,0-0.7l7.5-7.5c0.2-0.2,0.3-0.5,0.3-0.7s-0.1-0.5-0.3-0.7l-1.4-1.4C20,0.1,19.7,0,19.5,0  c-0.3,0-0.5,0.1-0.7,0.3l-7.5,7.5c-0.2,0.2-0.5,0.2-0.7,0L3.1,0.3C2.9,0.1,2.6,0,2.4,0S1.9,0.1,1.7,0.3L0.3,1.7C0.1,1.9,0,2.2,0,2.4  s0.1,0.5,0.3,0.7l7.5,7.5c0.2,0.2,0.2,0.5,0,0.7l-7.5,7.5C0.1,19,0,19.3,0,19.5s0.1,0.5,0.3,0.7l1.4,1.4c0.2,0.2,0.5,0.3,0.7,0.3  s0.5-0.1,0.7-0.3l7.5-7.5c0.2-0.2,0.5-0.2,0.7,0l7.5,7.5c0.2,0.2,0.5,0.3,0.7,0.3s0.5-0.1,0.7-0.3l1.4-1.4c0.2-0.2,0.3-0.5,0.3-0.7  s-0.1-0.5-0.3-0.7L14.1,11.3z"/>
    </svg>`;

    let number = $('.competency-pill').length;

    //console.log($('#competencies').children().length)
    if ($('#competencies').children().length == 1) {
      $('.competencies-placeholder').addClass('competencies-placeholder-hidden');
    }

    $('#competencies').append(`<input type="hidden" value="${value}" name="competency-${number}-competency" id="id_competency-${number}-competency" /><span class="competency-pill">${title} <span class="competency-pill-close">${svg}</span></span>`);

    let addedItem = $('#competencies').children('span').last();

    setTimeout(() => {
      $(addedItem).addClass('competency-pill-visible');
    }, 0);


    // Then hide just selected option
    $(selected).attr('hidden', 'true');
  });

  $(document).on('click', '.competency-pill-close', e => {
    let pill = $(e.target).closest('.competency-pill');
    let inputHidden = $(pill).prev();
    let value = parseInt($(pill).prev().val());

    $(`#competencies-select option[value="${value}"]`).removeAttr('hidden');
    $(pill).remove();

    $(inputHidden).remove();

    let inputsAmount = $('input[name="competency-TOTAL_FORMS"]').val();
    $('input[name="competency-TOTAL_FORMS"]').val(--inputsAmount);
    recountHiddenInputs();

  });
});
