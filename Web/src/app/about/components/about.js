define('app/about/components/about',['require','text!app/templates/about/about.html', 'knockout'], function(require, template) {
  'use strict';

  function ViewAbout() {
    this.title = 'Welcome';
  }


  return {
    viewModel: ViewAbout,
    template: template
  };
});
