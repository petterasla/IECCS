define('app/visualization/components/bar-chart/bar-chart' ,['require','knockout', 'c3', 'd3', '$http', 'q', 'text!app/templates/visualization/bar.html'], function(require, ko, c3, d3, $http, $q, template) {
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

  function ViewBar() {
    var initFavor = [];
    var initAgainst = [];
    var initNone = [];
    var self = this;
    self.alert = ko.observable(0);
    self.alertMsg = ko.observable('Error retrieving some of the data!');
    self.progress = ko.observable(5);
    self.progressPct = ko.observable('5%');
    console.log(self.progress());

    var favorReq = $http.get('https://ieccs.herokuapp.com/api/stance/year/FAVOR')
      .success(function(data) {
        initFavor = data;
        self.progress(self.progress()+30);
        self.progressPct(self.progress()+'%');
        console.log(self.progress());
      })
      .error(function(err) {
        self.alert(1);
        console.log(err);
      });
    var againstReq = $http.get('https://ieccs.herokuapp.com/api/stance/year/AGAINST')
      .success(function(data) {
        initAgainst = data;
        self.progress(self.progress()+30);
        self.progressPct(self.progress()+'%');
        console.log(self.progress());
      })
      .error(function(err) {
        self.alert(1);
        console.log(err);
      });
    var noneReq = $http.get('https://ieccs.herokuapp.com/api/stance/year/NONE')
      .success(function(data) {
        initNone = data;
        self.progress(self.progress()+30);
        self.progressPct(self.progress()+'%');
        console.log(self.progress());
      })
      .error(function(err) {
        self.alert(1);
        console.log(err);
      });

    $q.all([favorReq, noneReq, againstReq]).then( function() {
      self.progress(self.progress()+5);
      self.progressPct(self.progress()+'%');
      console.log(self.progress());

      setTimeout(function(){
        self.progress(self.progress()+1);
        self.progressPct(self.progress()+'%');
        console.log(self.progress());
      }, 500);


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
    viewModel: ViewBar,
    template: template
  };
});
