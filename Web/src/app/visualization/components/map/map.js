define('app/visualization/components/map/map' ,
  ['require','knockout', '$http', 'q',
  'app/visualization/components/map/data', 'ammap', 'dark', 'worldLow'],
  function(require, ko, $http, $q, coordinates) {
  'use strict';

  function init() {
    var mapData = [];
    var latlong = coordinates;


    var dataReq = $http.get("https://ieccs.herokuapp.com/api/visual/organization/All")
      .success(function (info) {
        mapData = info.Data;
      })
      .error(function (err) {
        console.log(err)
      });

    $q.all([dataReq]).then(function () {
      var minBulletSize = 6;
      var maxBulletSize = 70;
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

      console.log("building map");

      window.map = new AmCharts.AmMap();
      AmCharts.theme = AmCharts.themes.dark;

      window.map.addTitle("Organization countries", 14);
      window.map.addTitle("from TCP data", 11);
      window.map.areasSettings = {
        unlistedAreasColor: "#000000",
        unlistedAreasAlpha: 0.1
      };
      window.map.imagesSettings.balloonText = "<span style='font-size:14px;'><b>[[title]]</b>: [[value]]</span>";
      var dataProvider = {
        mapVar: AmCharts.maps.worldLow,
        images: []
      };

      // create circle for each country


      // it's better to use circle square to show difference between values, not a radius
      var maxSquare = maxBulletSize * maxBulletSize * 2 * Math.PI;
      var minSquare = minBulletSize * minBulletSize * 2 * Math.PI;

      // create circle for each country
      for (var i = 0; i < mapData.length; i++) {
        var dataItem = mapData[i];
        var value = dataItem.value;
        // calculate size of a bubble
        var square = (value - min) / (max - min) * (maxSquare - minSquare) + minSquare;
        if (square < minSquare) {
          square = minSquare;
        }
        var size = Math.sqrt(square / (Math.PI * 2));
        var id = dataItem.code;
        dataProvider.images.push({
          type: "circle",
          width: size,
          height: size,
          color: dataItem.color,
          longitude: latlong[id].longitude,
          latitude: latlong[id].latitude,
          title: dataItem.name,
          value: value
        });

      }


      // the following code uses circle radius to show the difference
      /*
       for (var i = 0; i < mapData.length; i++) {
       var dataItem = mapData[i];
       var value = dataItem.value;
       // calculate size of a bubble
       var size = (value - min) / (max - min) * (maxBulletSize - minBulletSize) + minBulletSize;
       if (size < minBulletSize) {
       size = minBulletSize;
       }
       var id = dataItem.code;

       dataProvider.images.push({
       type: "circle",
       width: size,
       height: size,
       color: dataItem.color,
       longitude: latlong[id].longitude,
       latitude: latlong[id].latitude,
       title: dataItem.name,
       value: value
       });
       }*/

      window.map.dataProvider = dataProvider;
      window.map.export = {
        enabled: true
      };
      window.map.projection = "miller";
      window.map.write("chartdiv");
      console.log("gon trhoug everything");
    })
  }


  return {
    viewModel: init(),
    template: '<div id="chartdiv"></div>'
  }

});



