define('app/about/components/about',['require', 'knockout', 'app/templates/about/about'], function(require) {
  'use strict';

  var ko   = require('knockout');

  function ViewAbout() {

  }


  return {
    viewModel: ViewAbout,
    template: require('app/templates/about/about')
  };
});
