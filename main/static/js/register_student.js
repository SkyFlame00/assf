function recountEducItems() {
  $('.education-form').children().length;

  let items = $('.education-form');

  let i = 1;

  // for (let item of items) {
  //   if (i < numClicked) {
  //     i++;
  //     continue;
  //   }
  //
  //   let info = $(item).children()[0];
  //
  //   $(info).find('.signup-educ-item-num span').css({
  //     'transform': 'translateX(30px)',
  //     'opacity': '0',
  //     'visibility': 'hidden'
  //   });
  //
  //   let m = i;
  //   setTimeout(() => {
  //
  //     $(info).find('.signup-educ-item-num').prepend('<span class="signup-educ-item-num-hidden">#' + m + '</span>');
  //     $(info).find('.signup-educ-item-num span')[1].remove();
  //
  //     setTimeout(() => {
  //       $(info).find('.signup-educ-item-num span').css({
  //         'visibility': 'visible',
  //         'opacity': '1',
  //         'transform': 'translateX(0)'
  //       });
  //     }, 20);
  //   }, 400);
  //
  //   i++;
  // }
  //
  // i = 1;

  for (let item of items) {
    let inputs = $(item).children('.registration-inputline');
    //console.log($(inputs[0]).find('label').attr('for'))
    $(inputs[0]).find('label').attr('for', 'id_form-' + (i - 1) +'-university');
    $(inputs[0]).find('input').attr('id', 'id_form-' + (i - 1) +'-university');
    $(inputs[0]).find('input').attr('name', 'form-' + (i - 1) +'-university');

    $(inputs[1]).find('label').attr('for', 'id_form-' + (i - 1) +'-degree');
    $(inputs[1]).find('select').attr('id', 'id_form-' + (i - 1) +'-degree');
    $(inputs[1]).find('select').attr('name', 'form-' + (i - 1) +'-degree');

    $(inputs[2]).find('label').attr('for', 'id_form-' + (i - 1) +'-programme');
    $(inputs[2]).find('select').attr('id', 'id_form-' + (i - 1) +'-programme');
    $(inputs[2]).find('select').attr('name', 'form-' + (i - 1) +'-programme');

    $(inputs[3]).find('label').attr('for', 'id_form-' + (i - 1) +'-year_start');
    $(inputs[3]).find('input').attr('id', 'id_form-' + (i - 1) +'-year_start');
    $(inputs[3]).find('input').attr('name', 'form-' + (i - 1) +'-year_start');

    $(inputs[4]).find('label').attr('for', 'id_form-' + (i - 1) +'-year_end');
    $(inputs[4]).find('input').attr('id', 'id_form-' + (i - 1) +'-year_end');
    $(inputs[4]).find('input').attr('name', 'form-' + (i - 1) +'-year_end');

    i++;
  }
}

function recountJobItems() {
  $('.job-form').children().length;
  let items = $('.job-form');
  let i = 1;

  for (let item of items) {
    let inputs = $(item).children('.registration-inputline');
    $(inputs[0]).find('label').attr('for', 'id_job-' + (i - 1) +'-company');
    $(inputs[0]).find('select').attr('id', 'id_job-' + (i - 1) +'-company');
    $(inputs[0]).find('select').attr('name', 'job-' + (i - 1) +'-company');

    $(inputs[1]).find('label').attr('for', 'id_job-' + (i - 1) +'-position');
    $(inputs[1]).find('input').attr('id', 'id_job-' + (i - 1) +'-position');
    $(inputs[1]).find('input').attr('name', 'job-' + (i - 1) +'-position');

    $(inputs[2]).find('label').attr('for', 'id_job-' + (i - 1) +'-year_start');
    $(inputs[2]).find('input').attr('id', 'id_job-' + (i - 1) +'-year_start');
    $(inputs[2]).find('input').attr('name', 'job-' + (i - 1) +'-year_start');

    $(inputs[3]).find('label').attr('for', 'id_job-' + (i - 1) +'-year_end');
    $(inputs[3]).find('input').attr('id', 'id_job-' + (i - 1) +'-year_end');
    $(inputs[3]).find('input').attr('name', 'job-' + (i - 1) +'-year_end');

    i++;
  }
}

// For competencies adding
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
  let educFormsAmount = $('.education-form').length;
  let jobFormsAmount = $('.job-form').length;

  if (educFormsAmount > 1) {
    $('.education-form').find('.education-form-info').removeClass('education-form-info-hidden');
  }

  if (jobFormsAmount > 1) {
    $('.job-form').find('.job-form-info').removeClass('job-form-info-hidden');
  }

  $('#add-education').click(e => {
    let educFormsAmount = $('.education-form').length;

    if (educFormsAmount > 1) {
      for (let item of $('.education-form')) {
        $(item).removeClass('education-form-info-hidden');
      }
    }

    let formsAmount = parseInt($('input[name="form-TOTAL_FORMS"]').val());
    $('input[name="form-TOTAL_FORMS"]').val(++formsAmount);

    $.ajax({
      url: '/get-universities/',
      success: result => {
        result = JSON.parse(result);
        universities = [];

        for (let key of Object.keys(result)) {
          universities.push(result[key]);
        }

        let str = '<option value="" selected="">---------</option>';

        for (let i = 0; i < universities.length; i++) {
          str += `<option value="${universities[i].id}">${universities[i].title}</option>`;
        }

        let html = `
                  <div class="education-form">

                    <div class="education-form-info">
                      <div class="education-form-del">
                        <span class="delete-education">
                          <svg version="1.1" id="Capa_1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px" width="408.483px" height="408.483px" viewBox="0 0 408.483 408.483" style="enable-background:new 0 0 408.483 408.483;" xml:space="preserve">
                            <g>
                              <path d="M87.748,388.784c0.461,11.01,9.521,19.699,20.539,19.699h191.911c11.018,0,20.078-8.689,20.539-19.699l13.705-289.316
                                H74.043L87.748,388.784z M247.655,171.329c0-4.61,3.738-8.349,8.35-8.349h13.355c4.609,0,8.35,3.738,8.35,8.349v165.293
                                c0,4.611-3.738,8.349-8.35,8.349h-13.355c-4.61,0-8.35-3.736-8.35-8.349V171.329z M189.216,171.329
                                c0-4.61,3.738-8.349,8.349-8.349h13.355c4.609,0,8.349,3.738,8.349,8.349v165.293c0,4.611-3.737,8.349-8.349,8.349h-13.355
                                c-4.61,0-8.349-3.736-8.349-8.349V171.329L189.216,171.329z M130.775,171.329c0-4.61,3.738-8.349,8.349-8.349h13.356
                                c4.61,0,8.349,3.738,8.349,8.349v165.293c0,4.611-3.738,8.349-8.349,8.349h-13.356c-4.61,0-8.349-3.736-8.349-8.349V171.329z"></path>
                              <path d="M343.567,21.043h-88.535V4.305c0-2.377-1.927-4.305-4.305-4.305h-92.971c-2.377,0-4.304,1.928-4.304,4.305v16.737H64.916
                                c-7.125,0-12.9,5.776-12.9,12.901V74.47h304.451V33.944C356.467,26.819,350.692,21.043,343.567,21.043z"></path>
                            </g>
                          </svg>
                        </span>
                      </div>
                    </div>

                    <div class="registration-inputline-wrapper choose-university">
                      <div class="registration-inputline clearfix university">
                        <div class="registration-inputline-labelblock">
                          <label for="id_form-${formsAmount}-university">Университет</label>
                        </div>
                        <div class="registration-inputline-inputblock">
                          <select name="form-${formsAmount}-university" id="id_form-${formsAmount}-university">
                    <option value="" selected="">---------</option>

                    ${str}

                    </select>
                        </div>
                      </div>


                    </div>

                    <div class="registration-inputline-wrapper choose-degree">
                      <div class="registration-inputline clearfix university degree">
                        <div class="registration-inputline-labelblock">
                          <label for="id_form-${formsAmount}-degree">Ступень обучения</label>
                        </div>
                        <div class="registration-inputline-inputblock">
                          <select name="form-${formsAmount}-degree" id="id_form-${formsAmount}-degree">
                    <option value="bac">Бакалавриат</option>

                    <option value="mag">Магистратура</option>

                    </select>
                        </div>
                      </div>


                    </div>

                    <div class="registration-inputline-wrapper choose-program">
                      <div class="registration-inputline clearfix university">
                        <div class="registration-inputline-labelblock">
                          <label for="id_form-${formsAmount}-program">Направление обучения</label>
                        </div>
                        <div class="registration-inputline-inputblock">
                          <select name="form-${formsAmount}-program" id="id_form-${formsAmount}-program">
                    <option value="" selected="">---------</option>

                    </select>
                        </div>
                      </div>


                    </div>

                    <div class="registration-inputline-wrapper choose-program">
                      <div class="registration-inputline clearfix university year_start">
                        <div class="registration-inputline-labelblock">
                          <label for="id_form-${formsAmount}-year_start">Год начала</label>
                        </div>
                        <div class="registration-inputline-inputblock">
                          <input type="number" name="form-${formsAmount}-year_start" id="id_form-${formsAmount}-year_start">
                        </div>
                      </div>
                    </div>

                    <div class="registration-inputline-wrapper choose-program">
                      <div class="registration-inputline clearfix university year_end">
                        <div class="registration-inputline-labelblock">
                          <label for="id_form-${formsAmount}-year_end">Год окончания</label>
                        </div>
                        <div class="registration-inputline-inputblock">
                          <input type="number" name="form-${formsAmount}-year_end" id="id_form-${formsAmount}-year_end">
                        </div>
                      </div>
                    </div>
                  </div>
        `;

        $('#education-forms').append(html);

        for (let item of $('.education-form')) {
          console.log($(item).find('.education-form-info'))
          $(item).find('.education-form-info').removeClass('education-form-info-hidden');
        }
      }
    });

  });

  $(document).on('click', '.delete-education', e => {
    //let numClicked = parseInt($(e.target).closest('.signup-educ-item-info').find('.signup-educ-item-num span').html().match(/\d+/)[0]);

    let formsAmount = parseInt($('input[name="form-TOTAL_FORMS"]').val());
    $('input[name="form-TOTAL_FORMS"]').val(--formsAmount);

    $(e.target).closest('.education-form').remove();
    recountEducItems();

    let educFormsAmount = $('.education-form').length;

    if (educFormsAmount < 2) {
      $('.education-form').find('.education-form-info').addClass('education-form-info-hidden');
    }
  });

  $(document).on('change', '.choose-university select', e => {
    let that = e.target;
    let university = parseInt($(that).find('option:selected').val());
    let degree = $(that).closest('.education-form').find('.choose-degree select option:selected').val();

    let data = {
      university: university,
      degree: degree
    };

    $.ajax({
      url: '/get-programs/',
      data: data,
      success: result => {
        result = JSON.parse(result);
        programs = [];

        for (let key of Object.keys(result)) {
          programs.push(result[key]);
        }

        let str = '<option value="" selected="">---------</option>';

        for (let i = 0; i < programs.length; i++) {
          str += `<option value="${programs[i].id}">${programs[i].title}</option>`;
        }

        $(that).closest('.education-form').find('.choose-program select').html(str);
      }
    });

  });

  $(document).on('change', '.choose-degree select', e => {
    let that = e.target;
    let university = $(that).closest('.education-form').find('.choose-university option:selected').val();
    console.log('value is ' + university);

    if (university == '') {
      $(that).closest('.education-form').find('.choose-program select').html('<option value="" selected="">---------</option>');
      return;
    }

    let degree = $(that).find('option:selected').val();

    let data = {
      university: university,
      degree: degree
    };

    $.ajax({
      url: '/get-programs/',
      data: data,
      success: result => {
        result = JSON.parse(result);
        programs = [];

        for (let key of Object.keys(result)) {
          programs.push(result[key]);
        }

        let str = '<option value="" selected="">---------</option>';

        for (let i = 0; i < programs.length; i++) {
          str += `<option value="${programs[i].id}">${programs[i].title}</option>`;
        }

        $(that).closest('.education-form').find('.choose-program select').html(str);
      }
    });
  });

  // Job handlers
  $('#add-job').click(e => {
    let jobFormsAmount = $('.job-form').length;

    let formsAmount = parseInt($('input[name="job-TOTAL_FORMS"]').val());
    $('input[name="job-TOTAL_FORMS"]').val(++formsAmount);

    $.ajax({
      url: '/get-companies/',
      success: result => {
        result = JSON.parse(result);
        companies = [];

        for (let key of Object.keys(result)) {
          companies.push(result[key]);
        }

        let str = '<option value="" selected="">---------</option>';

        for (let i = 0; i < companies.length; i++) {
          str += `<option value="${companies[i].id}">${companies[i].name}</option>`;
        }

        let html = `
                    <div class="job-form">

                    <div class="job-form-info job-form-info-hidden">
                    <div class="job-form-del">
                      <span class="delete-job">
                        <svg version="1.1" id="Capa_1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px" width="408.483px" height="408.483px" viewBox="0 0 408.483 408.483" style="enable-background:new 0 0 408.483 408.483;" xml:space="preserve">
                          <g>
                            <path d="M87.748,388.784c0.461,11.01,9.521,19.699,20.539,19.699h191.911c11.018,0,20.078-8.689,20.539-19.699l13.705-289.316
                              H74.043L87.748,388.784z M247.655,171.329c0-4.61,3.738-8.349,8.35-8.349h13.355c4.609,0,8.35,3.738,8.35,8.349v165.293
                              c0,4.611-3.738,8.349-8.35,8.349h-13.355c-4.61,0-8.35-3.736-8.35-8.349V171.329z M189.216,171.329
                              c0-4.61,3.738-8.349,8.349-8.349h13.355c4.609,0,8.349,3.738,8.349,8.349v165.293c0,4.611-3.737,8.349-8.349,8.349h-13.355
                              c-4.61,0-8.349-3.736-8.349-8.349V171.329L189.216,171.329z M130.775,171.329c0-4.61,3.738-8.349,8.349-8.349h13.356
                              c4.61,0,8.349,3.738,8.349,8.349v165.293c0,4.611-3.738,8.349-8.349,8.349h-13.356c-4.61,0-8.349-3.736-8.349-8.349V171.329z"></path>
                            <path d="M343.567,21.043h-88.535V4.305c0-2.377-1.927-4.305-4.305-4.305h-92.971c-2.377,0-4.304,1.928-4.304,4.305v16.737H64.916
                              c-7.125,0-12.9,5.776-12.9,12.901V74.47h304.451V33.944C356.467,26.819,350.692,21.043,343.567,21.043z"></path>
                          </g>
                        </svg>
                      </span>
                    </div>
                    </div>

                    <div class="registration-inputline-wrapper choose-program">
                    <div class="registration-inputline clearfix university">
                      <div class="registration-inputline-labelblock">
                        <label for="id_job-${jobFormsAmount}-company">Компания</label>
                      </div>
                      <div class="registration-inputline-inputblock">
                        <select name="job-${jobFormsAmount}-company" id="id_job-${jobFormsAmount}-company">
                    ${str}

                    </select>
                      </div>
                    </div>


                    </div>

                    <div class="registration-inputline-wrapper choose-program">
                    <div class="registration-inputline clearfix university">
                      <div class="registration-inputline-labelblock">
                        <label for="id_job-${jobFormsAmount}-position">Должность</label>
                      </div>
                      <div class="registration-inputline-inputblock">
                        <input type="text" name="job-${jobFormsAmount}-position" maxlength="60" id="id_job-${jobFormsAmount}-position">
                      </div>
                    </div>


                    </div>

                    <div class="registration-inputline-wrapper choose-program">
                    <div class="registration-inputline clearfix university year_start">
                      <div class="registration-inputline-labelblock">
                        <label for="id_job-${jobFormsAmount}-year_start">Год начала</label>
                      </div>
                      <div class="registration-inputline-inputblock">
                        <input type="number" name="job-${jobFormsAmount}-year_start" id="id_job-${jobFormsAmount}-year_start">
                      </div>
                    </div>


                    </div>

                    <div class="registration-inputline-wrapper choose-program">
                    <div class="registration-inputline clearfix university year_end">
                      <div class="registration-inputline-labelblock">
                        <label for="id_job-0-year_end">Год окончания</label>
                      </div>
                      <div class="registration-inputline-inputblock">
                        <input type="number" name="job-${jobFormsAmount}-year_end" id="id_job-${jobFormsAmount}-year_end">
                      </div>
                    </div>


                    </div>


                    </div>
        `;

        $('#job-forms').append(html);

        for (let item of $('.job-form')) {
          console.log($(item).find('.job-form-info'))
          $(item).find('.job-form-info').removeClass('job-form-info-hidden');
        }
      }
    });
  });

  $(document).on('click', '.delete-job', e => {
    let formsAmount = parseInt($('input[name="job-TOTAL_FORMS"]').val());
    $('input[name="job-TOTAL_FORMS"]').val(--formsAmount);

    $(e.target).closest('.job-form').remove();
    recountJobItems();

    let jobFormsAmount = $('.job-form').length;

    if (jobFormsAmount < 2) {
      $('.job-form').find('.job-form-info').addClass('job-form-info-hidden');
    }
  });

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
