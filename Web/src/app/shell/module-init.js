define('app/shell/module-init', ['require', '$router', 'knockout'], function(require) {
  'use strict';

  function init() {
    var router = require('$router'),
        ko     = require('knockout');

    ko.components.register('main-nav', {
      require: 'app/shell/components/main-nav'
    });

    router.when('/', {
      viewModelUrl: 'app/shell/home/home',
      templateUrl: 'app/templates/home'
    }).otherwise({
      redirectTo: '/'
    });
  }

  return {
    init: init
  };
});
