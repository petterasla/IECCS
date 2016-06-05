define('app/about/module-init', ['require', 'knockout', '$router'], function(require, ko, router) {
  'use strict';
  var t, n, init;

  t = function() {
    return ko.components.register('about', {
      require: 'app/about/components/about'
    });
  };

  n = function() {
    return router.when('/about/', {
      templateUrl: 'text!app/templates/about/about.html',
      viewModelUrl: 'app/about/components/about'
    });
  };

  init = function() {
    n();
    t();
  };

  return{ init: init };
});
