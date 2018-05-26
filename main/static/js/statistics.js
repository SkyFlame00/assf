$(document).ready(() => {
  $.ajax({
    url: '/get_top10competencies_bycompanies/',
    success: result => {
      result = JSON.parse(result);
      let labels = [];
      let data = [];

      for (let item of result) {
        labels.push(item[0]);
        data.push(item[1]);
      }

      var ctx = document.getElementById("myChart");
      var myChart = new Chart(ctx, {
          type: 'horizontalBar',
          data: {
              labels: labels,
              datasets: [{
                  label: '%',
                  data: data,
                  backgroundColor: [
                      'rgba(255, 99, 132, 0.2)',
                      'rgba(54, 162, 235, 0.2)',
                      'rgba(255, 206, 86, 0.2)',
                      'rgba(75, 192, 192, 0.2)',
                      'rgba(153, 102, 255, 0.2)',
                      'rgba(255, 159, 64, 0.2)'
                  ],
                  borderColor: [
                      'rgba(255,99,132,1)',
                      'rgba(54, 162, 235, 1)',
                      'rgba(255, 206, 86, 1)',
                      'rgba(75, 192, 192, 1)',
                      'rgba(153, 102, 255, 1)',
                      'rgba(255, 159, 64, 1)'
                  ],
                  borderWidth: 1
              }]
          },
          options: {
            tooltips: {
                callbacks: {
                    label: function(tooltipItems, data) {
                        //return data.datasets[tooltipItems.datasetIndex].label +': ' + tooltipItems.yLabel + ' %';
                        return tooltipItems.xLabel + '%';
                    }
                }

            },
              scales: {
                  yAxes: [{
                      ticks: {
                          beginAtZero:true
                      },
                      scaleLabel: {
                          display: true,
                          labelString: 'Компетенции'
                      }
                  }],
                  xAxes: [{
                    ticks: {
                        beginAtZero:true,
                        min:0,
                        max: 15,
                        stepSize:10
                    },
                    scaleLabel: {
                        display: true,
                        labelString: 'Доли в процентах'
                    }
                  }]
              },
              legend: {
                display: false
              },

          }
      });


    }
  });


  $.ajax({
    url: '/get_top10companies_byvacancies/',
    success: result => {
      result = JSON.parse(result);
      let labels = [];
      let data = [];

      for (let item of result) {
        labels.push(item[0]);
        data.push(item[1]);
      }

      var ctx = document.getElementById("myChart2");
      var myChart = new Chart(ctx, {
          type: 'pie',
          data: {
              labels: labels,
              datasets: [{
                  label: '%',
                  data: data,
                  backgroundColor: [
                      'rgba(255, 99, 132, 0.2)',
                      'rgba(54, 162, 235, 0.2)',
                      'rgba(255, 206, 86, 0.2)',
                      'rgba(75, 192, 192, 0.2)',
                      'rgba(153, 102, 255, 0.2)',
                      'rgba(255, 159, 64, 0.2)'
                  ],
                  borderColor: [
                      'rgba(255,99,132,1)',
                      'rgba(54, 162, 235, 1)',
                      'rgba(255, 206, 86, 1)',
                      'rgba(75, 192, 192, 1)',
                      'rgba(153, 102, 255, 1)',
                      'rgba(255, 159, 64, 1)'
                  ],
                  borderWidth: 1
              }]
          }
      });
    }
  });


  $.ajax({
    url: '/get_top10universities_bystudents/',
    success: result => {
      result = JSON.parse(result);
      let labels = [];
      let data = [];

      for (let item of result) {
        labels.push(item[0]);
        data.push(item[1]);
      }

      var ctx = document.getElementById("myChart3");
      var myChart = new Chart(ctx, {
          type: 'doughnut',
          data: {
              labels: labels,
              datasets: [{
                  label: '%',
                  data: data,
                  backgroundColor: [
                      'rgba(255, 99, 132, 0.2)',
                      'rgba(54, 162, 235, 0.2)',
                      'rgba(255, 206, 86, 0.2)',
                      'rgba(75, 192, 192, 0.2)',
                      'rgba(153, 102, 255, 0.2)',
                      'rgba(255, 159, 64, 0.2)'
                  ],
                  borderColor: [
                      'rgba(255,99,132,1)',
                      'rgba(54, 162, 235, 1)',
                      'rgba(255, 206, 86, 1)',
                      'rgba(75, 192, 192, 1)',
                      'rgba(153, 102, 255, 1)',
                      'rgba(255, 159, 64, 1)'
                  ],
                  borderWidth: 1
              }]
          }
      });
    }
  });


  $.ajax({
    url: '/get_top10subjectsareasvacancies/',
    success: result => {
      result = JSON.parse(result);
      let labels = [];
      let data = [];

      for (let item of result) {
        labels.push(item[0]);
        data.push(item[1]);
      }

      var ctx = document.getElementById("myChart4");
      var myChart = new Chart(ctx, {
          type: 'bar',
          data: {
              labels: labels,
              datasets: [{
                  label: 'Число вакансий',
                  data: data,
                  backgroundColor: [
                      'rgba(255, 99, 132, 0.2)',
                      'rgba(54, 162, 235, 0.2)',
                      'rgba(255, 206, 86, 0.2)',
                      'rgba(75, 192, 192, 0.2)',
                      'rgba(153, 102, 255, 0.2)',
                      'rgba(255, 159, 64, 0.2)'
                  ],
                  borderColor: [
                      'rgba(255,99,132,1)',
                      'rgba(54, 162, 235, 1)',
                      'rgba(255, 206, 86, 1)',
                      'rgba(75, 192, 192, 1)',
                      'rgba(153, 102, 255, 1)',
                      'rgba(255, 159, 64, 1)'
                  ],
                  borderWidth: 1
              }]
          },
          options: {

              scales: {
                  yAxes: [{
                      ticks: {
                          beginAtZero:true
                      },
                      scaleLabel: {
                          display: true,
                          labelString: 'Области экономики'
                      }
                  }],
                  xAxes: [{
                    ticks: {
                        beginAtZero:true,
                        min:0,

                    },
                    scaleLabel: {
                        display: true,
                        labelString: 'Число вакансий'
                    }
                  }]
              },
              legend: {
                display: false
              }

          }
      });


    }
  });

});
