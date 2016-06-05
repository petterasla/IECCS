define('app/team/module-init', ['require', 'knockout', '$router'], function(require, ko, router) {
  'use strict';
  var t, n, init;

  t = function() {
    return ko.components.register('team', {
      require: 'app/team/components/team'
    });
  };

  n = function() {
    return router.when('/team/', {
      templateUrl: 'text!app/templates/team/team.html'
      //viewModelUrl: 'app/hello/view'
    });
  };

  init = function() {
    n();
    t();
  };

  return{ init: init };
});
