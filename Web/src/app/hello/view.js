define('app/hello/view', ['knockout', 'app/libs/libraries'], function(ko, libs) {
  'use strict';

  function n(input) {
    var lib = ko.utils.arrayFirst(libs, function(ko) {
      return ko.name === input.name;
    });

    this.title = ko.observable();
    this.name = ko.observable();

    this.title(lib.title || lib.name);
    this.name(lib.name);
  }
  return n;
});
