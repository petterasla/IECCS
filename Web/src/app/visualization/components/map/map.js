define('app/visualization/components/map/map' ,
  ['require','knockout', '$http', 'q', 'text!app/templates/visualization/map.html',
  'app/visualization/components/map/data','app/visualization/components/visualization-index/visualization-index' ,'ammap', 'dark', 'worldLow'],
  function(require, ko, $http, $q, template, coordinates, visModel) {
  'use strict';

    function requestData(stance, type_data, self) {
      var url;
      var data;
      var req;
      if (type_data == "Unseen data:") {
        if (stance === "All") {
          url = 'https://ieccs.herokuapp.com/api/visual/new/organization/' + stance
        }
        else {
          url = 'https://ieccs.herokuapp.com/api/visual/new/organization/' + stance.toUpperCase()
        }
      }
      else {
        if (stance === "All") {
          url = 'https://ieccs.herokuapp.com/api/visual/old/organization/' + stance
        }
        else {
          url = 'https://ieccs.herokuapp.com/api/visual/old/organization/' + stance.toUpperCase()
        }

      }
      req = $http.get(url)
        .success(function (info) {
          console.log('Data retrieved..');
          data = info.Data;
          updateBar(75, self);
          drawMap(data, type_data, self);
        })
        .error(function (err) {
          self.alert(1);
          console.log(err);
        });
    }

    function init() {
      var self = this;
      self.alert = ko.observable(0);
      self.progress = ko.observable(102);
      self.progressPct = ko.observable('0%');
      self.alertMsg = ko.observable('Error retrieving some of the data!');
      self.allStancesFalse = ko.observable(true);

      self.stanceModel = [
        {id: 0, type:'All', icon: '<i class="fa fa-globe"></i>', status: ko.observable(false)},
        {id: 1, type:'Favor', icon: '<i class="fa fa-thumbs-o-up"></i>', status: ko.observable(false)},
        {id: 2, type:'Against', icon: '<i class="fa fa-thumbs-o-down"></i>', status: ko.observable(false)},
        {id: 3, type:'None', icon: '<i class="fa fa-hand-o-right"></i>', status: ko.observable(false)}

      ];


      self.updateStanceStatus = function(index, visModel)  {
        console.log("progress = " + this.progress());
        updateBar(5, self);
        self.stanceModel.forEach(function(item) {
          if (index === item.id) {
            item.status(true);
            console.log('Requesting..');
            updateBar(25, self);
            requestData(item.type, visModel.type, self);
            self.allStancesFalse(false);

          }
          else {
            item.status(false);
          }
        });
      };


    }
    function updateBar(percentage, self) {
      self.progress(percentage);
      self.progressPct(self.progress() + "%");
      console.log("progress = " + self.progress());
      console.log("progressMSG = " + self.progressPct())
    }

    function drawMap(mapData, type_data, self) {
      console.log('Building map');
      updateBar(100, self);
      var latlong = coordinates;
      var minBulletSize = 6;
      var maxBulletSize = 60;
      var min = 1;
      var max = 7000;

      // build map

      window.map = new AmCharts.AmMap();
      AmCharts.theme = AmCharts.themes.dark;

      window.map.addTitle('Author countries', 14);
      window.map.addTitle('from '+type_data, 11);
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
      setTimeout(updateBar(102, self), 500);
    }


    return {
      viewModel: init,
      template: template
    };

});



