define('app/bar-chart/module-init', ['require', 'knockout', '$router'], function(require) {
  'use strict';
  var t, n, init, ko, router;

  ko = require('knockout');
  router = require('$router');

  t = function() {
    return ko.components.register('bar-chart', {
      require: 'app/bar-chart/components/bar-chart'
    });
  };

  n = function() {
    return router.when('/bar-chart/', {
      templateUrl: 'app/templates/bar-chart/bar-chart',
      viewModelUrl: 'app/bar-chart/components/bar-chart'
    });
  };

  init = function() {
    n();
    t();
  };

  return{ init: init };
});
