define('app/bar-chart/module-init', ['require', 'knockout', '$router'], function(require, ko, router) {
  'use strict';
  var t, n, init;

  t = function() {
    return ko.components.register('bar-chart', {
      require: 'app/bar-chart/components/bar-chart'
    });
  };

  n = function() {
    return router.when('/bar-chart/', {
      templateUrl: 'text!app/templates/bar-chart/bar-chart.html',
      viewModelUrl: 'app/bar-chart/components/bar-chart'
    });
  };

  init = function() {
    n();
    t();
  };

  return{ init: init };
});
