define('app/templates/hello/hello', [], function() {
  'use strict';

  return '<a href="#/hello/RequireJS"><button type="button" class="btn btn-default">Default</button></a>'; //'<div><blockquote data-bind="foreach: $data.description"><p><small data-bind="text: $data"></small></p></blockquote><br/><p><ul data-bind="foreach: $data.links" class="list-inline"><li class="text-center"><a data-bind="attr: {title: $data.title, href: $data.href}"><i data-bind="css: $data.iconClass" class="fa fa-2x"></i><br/><small data-bind="text: $data.linkText"></small></a></li></ul></p></div>';
});
