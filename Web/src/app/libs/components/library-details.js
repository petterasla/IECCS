define('app/libs/components/library-details', ['require', 'knockout', 'app/libs/libraries', 'app/templates/libs/library-details'], function(require) {
  'use strict';

  var ko = require('knockout'),
      libs = require('app/libs/libraries');

  function LibView(input) {
    var t = ko.unwrap(input.name),
      lib = ko.utils.arrayFirst(libs, function(input) {
        return input.name === t;
      });

    this.name = ko.observable();
    this.title = ko.observable();
    this.description = ko.observableArray();
    this.links = ko.observableArray();

    this.name(lib.name);
    this.title(lib.title || lib.name);
    this.description(lib.description);
    this.links(lib.links);
  }

  return {
    viewModel: LibView,
    template: require('app/templates/libs/library-details')
  };
});
