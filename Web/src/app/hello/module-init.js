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
      templateUrl: 'text!app/templates/hello/hello.html'
      //viewModelUrl: 'app/hello/view'
    }).when('/hello/{name}', {
      templateUrl: 'text!app/templates/hello/hello-view.html',
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
