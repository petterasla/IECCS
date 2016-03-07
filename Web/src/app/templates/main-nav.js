define('app/templates/main-nav', [], function() {
  'use strict';

  return  '<ul class="nav navbar-nav">' +
            '<li data-bind="css: {active: $data.currentLocation() === \'/\'}">' +
              '<a href="#/">Home</a>' +
            '</li>' +
            '<li data-bind="css: {active: $data.currentLocation() === \'/about/\'}">' +
              '<a href="#/about">About</a>' +
            '</li>' +
            '<li data-bind="css: {active: $data.currentLocation() === \'/bar-chart/\'}">' +
              '<a href="#/bar-chart">Visualization</a>' +
            '</li>' +
            '<li data-bind="css: {active: $data.currentLocation() === \'/hello/\'}">' +
              '<a href="#/hello/">Hello</a>' +
            '</li>' +
            '<li data-bind="css: {active: $data.currentLocation() === \'/libs/all/\'}">' +
              '<a href="#/libs/all/">Libraries</a>' +
            '</li>' +
          '</ul>' +
          '<ul class="nav navbar-nav pull-right">' +
            '<li>' +
              '<a href="https://github.com/crissdev/spa-template-ko/" title="GitHub Project" style="padding-top: 10.5px; padding-bottom: 10.5px">' +
                '<i class="fa fa-3x fa-github"></i>' +
              '</a>' +
            '</li>' +
          '</ul>';
});
