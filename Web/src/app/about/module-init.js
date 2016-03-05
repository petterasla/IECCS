define('app/about/module-init', ['require', 'knockout', '$router'], function(require) {
  'use strict';
  var t, n, init, ko, router;

  ko = require('knockout');
  router = require('$router');

  t = function() {
    return ko.components.register('about', {
      require: 'app/about/components/about'
    });
  };

  n = function() {
    return router.when('/about/', {
      templateUrl: 'app/templates/about/about',
      viewModelUrl: 'app/about/components/about'
    });
  };

  init = function() {
    n();
    t();
  };

  return{ init: init };
});
