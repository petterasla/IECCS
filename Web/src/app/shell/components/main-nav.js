define('app/shell/components/main-nav', ['require', '$router', 'app/templates/main-nav'], function(require) {
  'use strict';

  var router = require('$router');

  function init() {
    this.currentLocation = router.currentLocation;
  }

  return {
    viewModel: init,
    template: require('app/templates/main-nav')
  };
});
