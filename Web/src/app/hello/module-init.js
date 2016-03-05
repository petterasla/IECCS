define('app/hello/module-init', ['require', 'knockout', '$router'], function(require) {
  'use strict';
  var t, n, init, ko, router;

  ko = require('knockout');
  router = require('$router');

  t = function() {
    return ko.components.register('hello-world', {
      require: 'app/hello/components/helloWorld'
    });
  };

  n = function() {
    return router.when('/hello/', {
      templateUrl: 'app/templates/hello/hello'
      //viewModelUrl: 'app/hello/view'
    }).when('/hello/{name}', {
      templateUrl: 'app/templates/hello/hello-view',
      viewModelUrl: 'app/hello/view',
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
