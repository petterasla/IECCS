define('app/shell/home/home', ['knockout','q', '$http', 'c3'], function(ko, $q, $http, c3) {
  'use strict';

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

  function mergeDublicateYears(list) {
    var temp = {};
    var obj = null;
    for(var i=0; i < list.length; i++) {
      obj=list[i];

      if(!temp[obj._id]) {
        temp[obj._id] = obj;
      } else {
        temp[obj._id].count += obj.count;
      }
    }
    var result = [];
    for (var prop in temp) {
      result.push(temp[prop]);
    }
    return result
  }

  function HomeModel() {
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
        initFavor.push.apply(initFavor, data);
        self.progress(self.progress()+15);
        self.progressPct(self.progress()+'%');
        console.log(self.progress());
      })
      .error(function(err) {
        self.alert(1);
        console.log(err);
      });
    var againstReq = $http.get('https://ieccs.herokuapp.com/api/stance/year/AGAINST')
      .success(function(data) {
        initAgainst.push.apply(initAgainst, data);
        self.progress(self.progress()+15);
        self.progressPct(self.progress()+'%');
        console.log(self.progress());
      })
      .error(function(err) {
        self.alert(1);
        console.log(err);
      });
    var noneReq = $http.get('https://ieccs.herokuapp.com/api/stance/year/NONE')
      .success(function(data) {
        initNone.push.apply(initNone, data);
        self.progress(self.progress()+15);
        self.progressPct(self.progress()+'%');
        console.log(self.progress());
      })
      .error(function(err) {
        self.alert(1);
        console.log(err);
      });

    var favorReqNew = $http.get('https://ieccs.herokuapp.com/api/stance/year/FAVOR') //Change to new data
      .success(function(data) {
        initFavor.push.apply(initFavor, data);
        self.progress(self.progress()+15);
        self.progressPct(self.progress()+'%');
        console.log(self.progress());
      })
      .error(function(err) {
        self.alert(1);
        console.log(err);
      });
    var againstReqNew = $http.get('https://ieccs.herokuapp.com/api/stance/year/AGAINST') //Change to new data
      .success(function(data) {
        initAgainst.push.apply(initAgainst,data);
        self.progress(self.progress()+15);
        self.progressPct(self.progress()+'%');
        console.log(self.progress());
      })
      .error(function(err) {
        self.alert(1);
        console.log(err);
      });
    var noneReqNew = $http.get('https://ieccs.herokuapp.com/api/stance/year/NONE') //Change to new data
      .success(function(data) {
        initNone.push.apply(initNone, data);
        self.progress(self.progress()+15);
        self.progressPct(self.progress()+'%');
        console.log(self.progress());
      })
      .error(function(err) {
        self.alert(1);
        console.log(err);
      });


    $q.all([favorReq, noneReq, againstReq, favorReqNew, againstReqNew, noneReqNew]).then( function() {
      self.progress(self.progress()+5);
      self.progressPct(self.progress()+'%');
      console.log(self.progress());

      setTimeout(function(){
        self.progress(self.progress()+1);
        self.progressPct(self.progress()+'%');
        console.log(self.progress());
      }, 500);

      initFavor = initFavor.sort(compare);
      initAgainst = initAgainst.sort(compare);
      initNone = initNone.sort(compare);

      initFavor = mergeDublicateYears(initFavor);
      initAgainst = mergeDublicateYears(initAgainst);
      initNone = mergeDublicateYears(initNone);


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

  return HomeModel;
});
