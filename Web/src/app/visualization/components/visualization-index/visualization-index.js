define('app/visualization/components/visualization-index/visualization-index', ['require', 'knockout', '$router','text!app/templates/visualization/visualization-index.html'], function(require, ko, router, template) {
  'use strict';
  let self = this;
  let init = function() {
    let self = this; //If access is needed in i.e. function, send as parameter
    this.representation = [
      {id: 0, type: "Bar Chart", icon:'<i class="fa fa-bar-chart fa-2x pull-right"></i>', status: ko.observable(true)},
      {id: 1, type: "Graph", icon: '<i class="fa fa-line-chart fa-2x pull-right"></i>',status: ko.observable(false)},
      {id: 2, type: "Map", icon: '<i class="fa fa-globe fa-2x pull-right"></i>',status: ko.observable(false)}
    ];
    this.visualModel = [
      {id: 0, type: "Stance", status: ko.observable(false), template: `<div data-bind="component: 'bar-chart'"></div>` },
      {id: 1, type: "Year", status: ko.observable(false), template: `<div class="jumbotron"><h2> Year option comming</h2></div>`},
      {id: 2, type: "New Data", status: ko.observable(false), template: `<div class="jumbotron"><h2> New Data option comming</h2></div>`},
      {id: 3, type: "Custom Search", status: ko.observable(false), template: `<div class="jumbotron"><h2> Cusomary search option comming</h2></div>`}
    ];
    this.allOptionsFalse = ko.observable(true);

    console.log(`allOptions: ${this.allOptionsFalse()}`);

    this.checkOptions = (index) => {
      console.log(`Updating visual model representation: ${index}`);
      let options = false;
      this.visualModel.forEach((item) => {
          if (item.id === index) {
            item.status(true);
            options = false;
            console.log(`check options ${options}`);
            this.allOptionsFalse(options);
          }
        else {
            item.status(false);
          }
      });


    };

    this.updateRepresentationStatus = (index) => {
      console.log(`Updating representation status with index = ${index}`);
      this.representation.forEach(function(item) {
        if (index === item.id) {
          console.log(`Setting ${item.type} to true`);
          item.status(true);
        }
        else {
          console.log(`Setting ${item.type} to false`);
          item.status(false);
        }
      });
    };
    this.getStance = () => {
      this.visualModel.stance(true);
      this.visualModel.year(false);
      this.visualModel.newData(false);
      this.visualModel.custom(false);
      this.visualModel.allOptionsFalse(false);
      console.log(`getStance click: ${this.visualModel.stance()}`);
    };

    this.getYear = () => {
      this.visualModel.stance(false);
      this.visualModel.year(true);
      this.visualModel.newData(false);
      this.visualModel.custom(false);
      this.visualModel.allOptionsFalse(false);
      console.log(`getYear click: ${this.visualModel.year()}`);
    };

    this.getNewData = () => {
      this.visualModel.stance(false);
      this.visualModel.year(false);
      this.visualModel.newData(true);
      this.visualModel.custom(false);
      this.visualModel.allOptionsFalse(false);
      console.log(`getNewData click: ${this.visualModel.newData()}`);
    };
    this.getCustom = () => {
      this.visualModel.stance(false);
      this.visualModel.year(false);
      this.visualModel.newData(false);
      this.visualModel.custom(true);
      this.visualModel.allOptionsFalse(false);
      console.log(`getCutsom click: ${this.visualModel.custom()}`);
    };

  };

  return {viewModel: init, template: template};
});
