define('app/libs/module-init', ['require', 'knockout', '$router'], function(require) {
  'use strict';
  var t, n, init, ko, router;

  ko = require('knockout');
  router = require('$router');

  t = function() {
    return ko.components.register('library-details', {
      require: 'app/libs/components/library-details'
    });
  };

  n = function() {
    return router.when('/libs/all/', {
      templateUrl: 'app/templates/libs/all',
      viewModelUrl: 'app/libs/all'
    }).when('/libs/view/{name}/', {
      templateUrl: 'app/templates/libs/view',
      viewModelUrl: 'app/libs/view',
      rules: {
        name: /^[-._a-z0-9 ]{1,30}$/i
      }
    });
  };

  init = function() {
    n();
    t();
  };

  return{ init: init };
});
