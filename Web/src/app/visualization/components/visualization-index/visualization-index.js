define('app/visualization/components/visualization-index/visualization-index', ['require', 'knockout', '$router','text!app/templates/visualization/visualization-index.html'], function(require, ko, router, template) {
  'use strict';
  var self = this;

  function init() {
    var self = this; //If access is needed in i.e. function, send as parameter

    self.representation = [
      {id: 0, type: 'Bar Chart', icon:'<i class="fa fa-bar-chart fa center"></i>', status: ko.observable(true)},
      {id: 1, type: 'Graph', icon: '<i class="fa fa-share-alt fa center"></i>',status: ko.observable(false)},
      {id: 2, type: 'Map', icon: '<i class="fa fa-globe fa center"></i>',status: ko.observable(false)}
    ];

    self.tmp = {repres:['bar-chart', 'graph', 'map']};

    self.visualModel = ko.observableArray([
      {id: 0, type: 'TCP data', icon: '<i class="fa fa-info-circle fa center"></i>', status: ko.observable(false), repres: self.tmp.repres },
      {id: 1, type: 'Unseen data', icon: '<i class="fa fa-question-circle fa center"></i>', status: ko.observable(false), repres: self.tmp.repres }
    ]);

    self.allOptionsFalse = ko.observable(true);

    //console.log(`allOptions: ${this.allOptionsFalse()}`);

    self.updateVisualNavBar = function(index) {
      //console.log(`Updating visual model representation: ${index}`);
      var options = false;
      self.visualModel().forEach(function(item) {
        if (item.id === index) {
          item.status(true);
          options = false;
          self.allOptionsFalse(options);
        }
        else {
            item.status(false);
        }
      });
    };

    self.updateRepresentationStatus = function(index) {
      //console.log(`Updating representation status with index = ${index}`);
      self.representation.forEach(function(item) {
        if (index === item.id) {
          //console.log(`Setting ${item.type} to true`);
          item.status(true);
        }
        else {
          //console.log(`Setting ${item.type} to false`);
          item.status(false);
        }
      });
    };
  }

  return {
    viewModel: init,
    template: template
  };
});
