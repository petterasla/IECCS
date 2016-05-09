define('app/visualization/module-init', ['require', 'knockout', '$router'], function(require, ko, router) {
  'use strict';
  var n, init;

  n = function() {
    ko.components.register('visualization-index', {
      require: 'app/visualization/components/visualization-index/visualization-index'
    });
    ko.components.register('bar-chart', {
      require: 'app/visualization/components/bar-chart/bar-chart'
    });
    ko.components.register('map', {
      require: 'app/visualization/components/map/map'
    });
    ko.components.register('graph', {
      require: 'app/visualization/components/graph/graph'
    });

    router.when('/visualization/', {
      templateUrl: 'text!app/templates/visualization/visualization-index.html',
      viewModelUrl: 'app/visualization/components/visualization-index/visualization-index'
    });
  };

  init = function() {
    n();
  };

  return{ init: init };
});
