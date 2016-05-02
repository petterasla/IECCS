define('app/visualization/components/visualization-index/visualization-index', ['require', 'knockout', '$router','text!app/templates/visualization/visualization-index.html'], function(require, ko, router, template) {
  'use strict';
  let self = this;

  let init = function() {
    let self = this; //If access is needed in i.e. function, send as parameter

    this.representation = [
      {id: 0, type: 'Bar Chart', icon:'<i class="fa fa-bar-chart fa center"></i>', status: ko.observable(true)},
      {id: 1, type: 'Graph', icon: '<i class="fa fa-line-chart fa center"></i>',status: ko.observable(false)},
      {id: 2, type: 'Map', icon: '<i class="fa fa-globe fa center"></i>',status: ko.observable(false)}
    ];

    this.tmp = {repres:['bar-chart', 'graph', 'map']};

    this.visualModel = [
      {id: 0, type: 'TCP data:', icon: '<i class="fa fa-info-circle fa center"></i>', status: ko.observable(false), repres: this.tmp.repres },
      {id: 1, type: 'Unseen data:', icon: '<i class="fa fa-question-circle fa center"></i>', status: ko.observable(false), repres: this.tmp.repres }
      //{id: 2, type: 'New Data', status: ko.observable(false), repres: this.tmp.repres },
      //{id: 3, type: 'Custom Search', status: ko.observable(false), repres: this.tmp.repres }
    ];

    this.allOptionsFalse = ko.observable(true);

    //console.log(`allOptions: ${this.allOptionsFalse()}`);

    this.updateVisualNavBar = (index) => {
      //console.log(`Updating visual model representation: ${index}`);
      let options = false;
      this.visualModel.forEach((item) => {
        if (item.id === index) {
        item.status(true);
        options = false;
        //console.log(`check options ${options}`);
        this.allOptionsFalse(options);
      }
    else {
        item.status(false);
      }
    });
    };

    this.updateRepresentationStatus = (index) => {
      //console.log(`Updating representation status with index = ${index}`);
      this.representation.forEach(function(item) {
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
  };

  return {
    viewModel: init,
    template: template
  };
});
