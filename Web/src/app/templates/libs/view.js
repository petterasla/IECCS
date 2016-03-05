define('app/templates/libs/view', [], function() {
  'use strict';

  return  '<div class="content-page-library-view">' +
            '<h2>' +
              '<a href="#/libs/all/" title="Back">' +
                '<i class="fa fa-arrow-circle-left back-button"></i>' +
              '</a>' +
              '&nbsp;' +
              '<span data-bind="text: $data.title"></span>' +
            '</h2>' +
            '<br/>' +
            '<library-details params="name: $data.name"></library-details>' +
          '</div>';
});
