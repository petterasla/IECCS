define('app/visualization/components/visualization-index/visualization-index', ['require', 'knockout', '$router','text!app/templates/visualization/visualization-index.html'], function(require, ko, router, template) {
  'use strict';

  let init = function() {
    this.visualModel = {
      stance: ko.observable(false),
      year: ko.observable(false),
      newData: ko.observable(false),
      custom: ko.observable(false),
      allOptionsFalse: ko.observable(true)
    };

    console.log(`allOptions: ${this.visualModel.allOptionsFalse()}`);

    this.checkOptions = () => {
      let options = this.visualModel.stance && this.visualModel.year && this.visualModel.newData && this.visualModel.custom;
      console.log(`check options ${options()}`);
      this.visualModel.allOptionsFalse(options());
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
