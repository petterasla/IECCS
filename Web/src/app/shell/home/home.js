define('app/shell/home/home', ['knockout','q', '$http'], function(ko, q, $http) {
  'use strict';

  function HomeModel() {

    this.showData = ko.observableArray(['Not doing anything']);

    this.getData = () => {
      var url = 'https://ieccs.herokuapp.com/api/data';
      this.showData('Watining for response...');
      console.log('http req');
      return $http.get(url)
        .success((data) => {
          console.log(data);
          this.showData(data);
        })
        .error((err) => {
          this.showData('Error. Something went wrong..');
          console.log(err);
        });
    };

  }
  return HomeModel;
});
