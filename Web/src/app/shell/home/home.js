define('app/shell/home/home', ['knockout','q', '$http'], function(ko, $q, $http) {
  'use strict';

  function HomeModel() {
    var self = this;
    var retData = null;

    self.showData = ko.observableArray(['Not doing anything']);

    self.getData = function () {
      console.log('http req');
      self.showData('Watining for response...');
      var request = $http.get('https://ieccs.herokuapp.com/api/stance/year/FAVOR')
        .success(function (data) {
          console.log('Success');
          retData = data;
        })
        .error(function (err) {
          console.log(err);
        });

      $q.all([request]).then(function () {
        self.showData(retData);
      });
    };
  }

  return HomeModel;
});
