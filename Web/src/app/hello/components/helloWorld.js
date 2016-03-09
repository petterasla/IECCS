define('app/hello/components/helloWorld',['require', 'knockout', 'app/libs/libraries'], function(require) {
  'use strict';

  var ko   = require('knockout'),
      libs = require('app/libs/libraries'),
      template = require(['text!app/templates/hello/hello-view.html'], function (temp) {
        return temp
      });

  function ViewContent() {
    var tool = libs[0];

    this.name = ko.observable();
    this.title = ko.observable();
    this.description = ko.observableArray();
    this.links = ko.observableArray();

    this.name(tool.name);
    this.title(tool.title || tool.name);
    this.description(tool.description);
    this.links(tool.links);
  }


  return {
    viewModel: ViewContent,
    template: template
  };
});
