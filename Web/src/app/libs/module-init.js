define('app/libs/module-init', ['require', 'knockout', '$router'], function(require, ko, router) {
  'use strict';
  var t, n, init;


  t = function() {
    return ko.components.register('library-details', {
      require: 'app/libs/components/library-details'
    });
  };

  n = function() {
    return router.when('/libs/all/', {
      templateUrl: 'text!app/templates/libs/all.html',
      viewModelUrl: 'app/libs/all'
    }).when('/libs/view/{name}/', {
      templateUrl: 'text!app/templates/libs/view.html',
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
