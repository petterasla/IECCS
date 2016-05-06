define('app/libs/all', ['knockout', 'app/libs/libraries'], function(ko, libs) {
  'use strict';

  function n() {
    this.title = ko.observable('Toolbox');
    this.libraries = libs.map(function(ko) {
      return {
        name: ko.name,
        title: ko.title || ko.name
      };
    });
  }

  return n;
});
