define('app/templates/home', [], function() {
  'use strict';

  return  '<h2 data-bind="text: $data.title"></h2>' +
          '<p style="margin-top: 30px">' +
            '<span>This is a simple demo showing how you can use this template to create a SPA easy and fast.</span>' +
          '</p>' +
          '<p>' +
            '<span>The libraries used to create this template are&nbsp;</span>' +
            '<a href="http://knockoutjs.com/">Knockout</a>' +
            '<span>,&nbsp;</span>' +
            '<a href="http://millermedeiros.github.io/crossroads.js/">Crossroads.js</a>' +
            '<span>,&nbsp;</span>' +
            '<a href="http://getbootstrap.com/">Bootstrap</a>' +
            '<span>,&nbsp;</span>' +
            '<a href="http://jquery.com/">jQuery</a>' +
            '<span>,&nbsp;</span>' +
            '<a href="http://fontawesome.io/">Font Awesome</a>' +
            '<span>&nbsp;and&nbsp;</span>' +
            '<a href="http://documentup.com/kriskowal/q/">Q</a>' +
            '<span>.</span>' +
          '</p>' +
          '<p>&nbsp;</p>' +
          '<h4>Install</h4>' +
          '<div class="panel panel-primary">' +
            '<div class="panel-heading">Github (Recommended)</div>' +
            '<div class="panel-body">' +
              '<code>git clone git://github.com/crissdev/spa-template-ko.git -b master spa-ko</code>' +
            '</div>' +
          '</div>' +
          '<div class="panel panel-default">' +
            '<div class="panel-heading">Bower</div>' +
            '<div class="panel-body"><code>bower install spa-template-ko</code></div>' +
          '</div>' +
          '<h4>Build</h4>' +
          '<div class="panel panel-primary">' +
            '<div class="panel-heading">Gulp</div>' +
            '<div class="panel-body">' +
              '<p>The build script supports a number of options that can be passed through command line. ' +
                  'Run\nthe following command in the application directory to see all the options available.\n' +
              '</p>' +
              '<code>gulp --help</code>' +
            '</div>' +
          '</div>' +
          '<h4>Test</h4>' +
          '<div class="panel panel-primary">' +
            '<div class="panel-heading">Karma</div>' +
            '<div class="panel-body">' +
              '<p>Tests can be run with Karma.</p>' +
              '<code>karma start</code>' +
            '</div>' +
          '</div>' +
        '</div>';
});
