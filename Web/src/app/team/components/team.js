define('app/team/components/team',['require', 'knockout', 'app/libs/libraries','text!app/templates/team/team.html'], function(require, ko, libs, template) {
  'use strict';

  function ViewTeam() {

  }


  return {
    viewModel: ViewTeam,
    template: template
  };
});
