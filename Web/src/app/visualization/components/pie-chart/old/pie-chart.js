define('app/visualization/components/pie-chart/old/pie-chart' ,['require','knockout', '$http', 'q',
  'amcharts', 'pie', 'light', 'animate.min'], function(require, ko, $http, $q) {
  'use strict';

  Object.size = function(obj) {
    var size = 0, key;
    for (key in obj) {
      if (obj.hasOwnProperty(key)) {
        size++;
      }
    }
    return size;
  };

  function compare(a,b) {
    a = parseInt(a._id);
    b = parseInt(b._id);
    if (a < b) {
      return -1;
    }
    else if (a > b) {
      return 1;
    }
    else {
      return 0;
    }
  }

  function init() {
    var initFavor = [];
    var initAgainst = [];
    var initNone = [];

    var favorReq = $http.get('https://ieccs.herokuapp.com/api/stance/year/FAVOR')
      .success(function (data) {
        initFavor = data;
      })
      .error(function (err) {
        console.log(err);
      });
    var againstReq = $http.get('https://ieccs.herokuapp.com/api/stance/year/AGAINST')
      .success(function (data) {
        initAgainst = data;
      })
      .error(function (err) {
        console.log(err);
      });
    var noneReq = $http.get('https://ieccs.herokuapp.com/api/stance/year/NONE')
      .success(function (data) {
        initNone = data;
      })
      .error(function (err) {
        console.log(err);
      });

    $q.all([favorReq, noneReq, againstReq]).then(function () {
      initFavor = initFavor.sort(compare);
      initNone = initNone.sort(compare);
      initAgainst = initAgainst.sort(compare);

      var favor = [];
      favor.push('Favor');
      favor = favor.concat(initFavor.map(function (a) {
        return a.count;
      }));

      var against = [];
      against.push('Against');
      against = against.concat(initAgainst.map(function (a) {
        return a.count;
      }));

      var none = [];
      none.push('None');
      none = none.concat(initNone.map(function (a) {
        return a.count;
      }));

      var keys = [];
      keys = initFavor.map(function (a) {
        return String(a._id);
      });

      var pieData = {};
      for (var i = 1; i < none.length; i++) {
        var total = none[i] + favor[i] + against[i] + 0.0;
        var key = keys[i-1];
        var aga = against[i];
        if (aga === 0) {
          aga = 0.0;
        } else {
          aga = (aga/total).toFixed(3);
        }
        pieData[key] =
          [
            {'sector': 'Favor', 'size': parseFloat((favor[i]/total).toFixed(3))},
            {'sector': 'Against', 'size': parseFloat(aga)},
            {'sector': 'None', 'size': parseFloat((none[i]/total).toFixed(3))}
          ];
      }
      /**
       * Create the chart
       */


      var currentYear = keys[0];
      var chart = AmCharts.makeChart( 'piechartdiv', {
        'type': 'pie',
        'theme': 'light',
        'dataProvider': [],
        'valueField': 'size',
        'titleField': 'sector',
        'startDuration': 0,
        'innerRadius': 80,
        'pullOutRadius': 20,
        'marginTop': 30,
        'titles': [{
          'text': 'Stance development over the years'
        }],
        'allLabels': [{
          'y': '54%',
          'align': 'center',
          'size': 25,
          'bold': true,
          'text': '1991',
          'color': '#555'
        }, {
          'y': '49%',
          'align': 'center',
          'size': 15,
          'text': 'Year',
          'color': '#555'
        }],
        'listeners': [ {
          'event': 'init',
          'method': function( e ) {
            var chart = e.chart;

            function getCurrentData() {
              var data = pieData[currentYear];
              currentYear++;
              if (currentYear > keys[keys.length-1]) {
                currentYear = keys[0];
              }
              return data;
            }

            function loop() {
              console.log('inside loop');
              chart.allLabels[0].text = currentYear;
              var data = getCurrentData();
              console.log(data[1].sector);
              console.log(data[1].size);
              chart.animateData( data, {
                duration: 800,
                complete: function() {
                  setTimeout( loop, 1200 );
                }
              } );
            }

            loop();
          }
        } ],
        'export': {
          'enabled': true
        }
      } );
    });
  }

  return {
    viewModel: init(),
    template: '<div id=piechartdiv></div>'
  };
});
