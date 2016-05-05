define('app/visualization/components/bar-chart/bar-chart' ,['require','knockout', 'c3', 'd3', '$http', 'q'], function(require, ko, c3, d3, $http, $q) {
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

  function ViewAbout() {
    var initFavor = [];
    var initAgainst = [];
    var initNone = [];

    var favorReq = $http.get('https://ieccs.herokuapp.com/api/stance/year/FAVOR')
      .success(function(data) {
        initFavor = data;
      })
      .error(function(err) {
        console.log(err);
      });
    var againstReq = $http.get('https://ieccs.herokuapp.com/api/stance/year/AGAINST')
      .success(function(data) {
        initAgainst = data;
      })
      .error(function(err) {
        console.log(err);
      });
    var noneReq = $http.get('https://ieccs.herokuapp.com/api/stance/year/NONE')
      .success(function(data) {
        initNone = data;
      })
      .error(function(err) {
        console.log(err);
      });

    $q.all([favorReq, noneReq, againstReq]).then( function() {
      initFavor = initFavor.sort(compare);
      initNone = initNone.sort(compare);
      initAgainst = initAgainst.sort(compare);

      var favor = [];
      favor.push('Favor');
      favor = favor.concat(initFavor.map(function (a) {return a.count;}));

      var against = [];
      against.push('Against');
      against = against.concat(initAgainst.map(function (a) {return a.count;}));

      var none = [];
      none.push('None');
      none = none.concat(initNone.map(function (a) {return a.count;}));

      var keys = [];
      keys = initFavor.map(function (a) {return parseInt(a._id);});

      var chart = c3.generate({
        bindto: '#BarChart',
        data: {
          columns: [
            favor,
            against,
            none
          ],
          type: 'bar',
          groups: [
            ['Favor', 'Against', 'None']
          ]
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
            categories: keys
          }
        }
      });
    });
  }

  return {
    viewModel: ViewAbout,
    template: '<div id="BarChart"></div>'
  }; //<div class="centered" data-bind="visible: notLoaded"><i class="fa fa-spinner fa-spin fa-5x"></i></div>
});
