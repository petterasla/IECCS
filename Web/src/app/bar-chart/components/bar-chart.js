define('app/bar-chart/components/bar-chart',['require', 'knockout', 'c3', 'd3', 'app/templates/bar-chart/bar-chart'], function(require) {
  'use strict';

  //var ko   = require('knockout');
  var c3   = require('c3');

  function ViewAbout() {
    var chart = setTimeout(c3.generate({
      data: {
        columns: [
          ['data1', 30, 200, 200, 400, 150, 250],
          ['data2', 130, 100, 100, 200, 150, 50],
          ['data3', 230, 200, 200, 300, 250, 250]
        ],
        type: 'bar',
        groups: [
          ['data1', 'data2', 'data3']
        ]
      },
      grid: {
        y: {
          lines: [{value:0}]
        }
      }
    }), 500);

    /*setTimeout(function () {
      chart.groups([['data1', 'data2', 'data3']]);
    }, 1000);

    setTimeout(function () {
      chart.load({
        columns: [['data4', 100, -50, 150, 200, -300, -100]]
      });
    }, 1500);

    setTimeout(function () {
      chart.groups([['data1', 'data2', 'data3', 'data4']]);
    }, 2000);*/
  }


  return {
    viewModel: ViewAbout,
    template: require('app/templates/bar-chart/bar-chart')
  };
});
