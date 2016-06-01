define('app/visualization/components/graph/graph' ,['require','knockout',
  'text!app/templates/visualization/graph.html'], function(require, ko, template) {
  'use strict';

  function init() {
    var self = this;
    self.graphModel = [
      {
        id: 0,
        size:'Large subset',
        type:'TCP data:',
        url:'https://graphcommons.com/graphs/85c23961-0213-44aa-b1a5-29de6a56df7a/embed',
        urlSmall:'https://graphcommons.com/graphs/4620d8a7-f393-45e8-b29b-45c2c7ed7893/embed',
        status:ko.observable(true)
      },
      {
        id: 1,
        size:'Large subset',
        type:'Unseen data:',
        url:'https://graphcommons.com/graphs/0d592f93-01ca-44d2-a3fe-3ce7d1b12a03/embed',
        urlSmall:'https://graphcommons.com/graphs/60f2202f-c226-4e3c-ad22-8e7c4be9f03b/embed',
        status:ko.observable(false)
      }
    ];
    self.url = ko.observable(self.graphModel[0].url);
    self.urlSmall = ko.observable(self.graphModel[0].urlSmall);

    self.updateUrl = function(dataType) {
      if (dataType.id === 1) {
        self.url(self.graphModel[1].url);
        self.urlSmall(self.graphModel[1].urlSmall);
      }
      else {
        self.url = ko.observable(self.graphModel[0].url);
        self.urlSmall = ko.observable(self.graphModel[0].urlSmall);
      }
    };
    self.toGraphCommon = function() {
      window.location.href = self.urlSmall();
    };
  }

  return {
    viewModel: init,
    template: template
  };
});
