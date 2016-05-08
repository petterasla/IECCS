define('app/data/components/data',['require', 'knockout','text!app/templates/data/data.html'], function(require, ko, template) {
  'use strict';

  function ViewTeam() {

  }


  return {
    viewModel: ViewTeam,
    template: template
  };
});
