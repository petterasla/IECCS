define('app/visualization/module-init', ['require', 'knockout', '$router'], function(require, ko, router) {
  'use strict';
  var t, n, init;


  t = function() {
    return ko.components.register('visualization-index', {
      require: 'app/visualization/components/visualization-index/visualization-index'
    });
  };


  n = function() {
    return router.when('/visualization/', {
      templateUrl: 'text!app/templates/visualization/visualization-index.html',
      viewModelUrl: 'app/visualization/components/visualization-index/visualization-index'
    });
  };

  init = function() {
    n();
    t();
  };

  return{ init: init };
});
