define('app/shell/components/main-nav', ['require', '$router', 'text!app/templates/main-nav.html'], function(require, router, template) {
  'use strict';

  function init() {
    this.currentLocation = router.currentLocation;
  }

  return {
    viewModel: init,
    template: template
  };
});
