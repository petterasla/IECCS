define('app/data/module-init', ['require', 'knockout', '$router'], function(require, ko, router) {
  'use strict';
  var t, n, init;

  t = function() {
    return ko.components.register('data', {
      require: 'app/data/components/data'
    });
  };

  n = function() {
    return router.when('/data/', {
      templateUrl: 'text!app/templates/data/data.html'
      //viewModelUrl: 'app/hello/view'
    });
  };

  init = function() {
    n();
    t();
  };

  return{ init: init };
});
