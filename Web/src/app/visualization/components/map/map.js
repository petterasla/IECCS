define('app/visualization/components/map/map' ,
  ['require','knockout', '$http', 'q', 'text!app/templates/visualization/map.html',
  'app/visualization/components/map/data', 'ammap', 'dark', 'worldLow'],
  function(require, ko, $http, $q, template, coordinates) {
  'use strict';

    function requestData(type) {
      var url;
      var data;
      var req;
      if (type === "All"){
        url = 'https://ieccs.herokuapp.com/api/visual/old/organization/'+type
      }
      else {
        url = 'https://ieccs.herokuapp.com/api/visual/old/organization/'+type.toUpperCase()
      }
      req = $http.get(url)
        .success(function(info) {
          data = info.Data;
          console.log('Data retrieved..');
          drawMap(data);
        })
        .error(function(err) {
          console.log(err);
        });
    }

    function init() {
      var self = this;

      self.allStancesFalse = ko.observable(true);

      self.stanceModel = [
        {id: 0, type:'All', icon: '<i class="fa fa-globe"></i>', status: ko.observable(false)},
        {id: 1, type:'Favor', icon: '<i class="fa fa-thumbs-o-up"></i>', status: ko.observable(false)},
        {id: 2, type:'Against', icon: '<i class="fa fa-thumbs-o-down"></i>', status: ko.observable(false)},
        {id: 3, type:'None', icon: '<i class="fa fa-hand-o-right"></i>', status: ko.observable(false)}

      ];

      self.updateStanceStatus = function(index)  {
        self.stanceModel.forEach(function(item) {
          if (index === item.id) {
            item.status(true);
            console.log('Requesting..');
            requestData(item.type);
            self.allStancesFalse(false);
          }
          else {
            item.status(false);
          }
        });
      };
    }

    function drawMap(mapData) {
      console.log('Building map');
      var latlong = coordinates;
      var minBulletSize = 6;
      var maxBulletSize = 60;
      var min = Infinity;
      var max = -Infinity;


      // get min and max values
      for (var i = 0; i < mapData.length; i++) {
        var value = mapData[i].value;
        if (value < min) {
          min = value;
        }
        if (value > max) {
          max = value;
        }
      }
      // build map

      window.map = new AmCharts.AmMap();
      AmCharts.theme = AmCharts.themes.dark;

      window.map.addTitle('Author countries', 14);
      window.map.addTitle('from TCP data', 11);
      window.map.areasSettings = {
        unlistedAreasColor: '#000000',
        unlistedAreasAlpha: 0.1
      };
      window.map.imagesSettings.balloonText = '<span style=font-size:14px;><b>[[title]]</b>: [[value]]</span>';
      var dataProvider = {
        mapVar: AmCharts.maps.worldLow,
        images: []
      };
      // create circle for each country
      // it's better to use circle square to show difference between values, not a radius
      var maxSquare = maxBulletSize * maxBulletSize * 2 * Math.PI;
      var minSquare = minBulletSize * minBulletSize * 2 * Math.PI;

      // create circle for each country
      for (var j = 0; j < mapData.length; j++) {
        var dataItem = mapData[j];
        var valueTwo = dataItem.value;
        // calculate size of a bubble
        var square = (valueTwo - min) / (max - min) * (maxSquare - minSquare) + minSquare;
        if (square < minSquare) {
          square = minSquare;
        }
        var size = Math.sqrt(square / (Math.PI * 2));
        var id = dataItem.code;
        dataProvider.images.push({
          type: 'circle',
          width: size,
          height: size,
          color: dataItem.color,
          longitude: latlong[id].longitude,
          latitude: latlong[id].latitude,
          title: dataItem.name,
          value: valueTwo
        });

      }
      window.map.dataProvider = dataProvider;
      window.map.export = {
        enabled: true
      };

      window.map.projection = 'miller';
      window.map.write('chartdiv');
    }


    return {
      viewModel: init,
      template: template
    };

});



