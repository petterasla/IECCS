define('app/visualization/components/bar-chart/bar-chart',['require', 'knockout', '../../../../c3', 'd3', 'app/visualization/components/bar-chart/data'], function(require, ko, c3, d3, data) {
  'use strict';

  Array.prototype.getUnique = function(){
    var u = {}, a = [];
    for(var i = 0, l = this.length; i < l; ++i){
      if(u.hasOwnProperty(this[i])) {
        continue;
      }
      a.push(this[i]);
      u[this[i]] = 1;
    }
    return a;
  };

  function ViewAbout() {
    var xValues = [];
    var arrayLength = data.length;
    for (var i = 0; i < arrayLength; i++) {
        xValues.push(parseInt(data[i].Year));
    }


    let chart = c3.generate({
      bindto: '#BarChart',
      data: {
        columns: [
          ['Favor', 1, 2],
          ['Against', 0, 1],
          ['None', 1, 0]
        ],
        type: 'bar',
        groups: [
          ['Favor', 'Against', 'None']
        ]
        //onclick: null
      },
      grid: {
        y: {
          lines: [{value:0}]
        }
      },
      axis: {
        x: {
          label: {
            text: 'Year',
            position: 'outer-center'
          },
          type: 'category',
          categories: xValues.getUnique()
        }
      }
    });

    /*
    setTimeout(function () {
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
    template: '<div id="BarChart"></div>'
  };
});

