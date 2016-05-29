define('app/visualization/components/map/map' ,
  ['require','knockout', '$http', 'q', 'text!app/templates/visualization/map.html',
  'app/visualization/components/map/data' ,'ammap', 'dark', 'worldLow'],
  function(require, ko, $http, $q, template, coordinates) {
  'use strict';


    function compare(a,b) {
      a = parseInt(a.value);
      b = parseInt(b.value);
      if (a > b) {
        return -1;
      }
      else if (a < b) {
        return 1;
      }
      else {
        return 0;
      }
    }

    function setColor(data, color) {
      data.forEach(function(item) {
        item.color = color;
      });
      return data;
    }

    function requestData(stance, typeData, self) {
      var url, url1, url2, url3;
      var data;
      var req, req1, req2, req3;
      var favorColor = '#2ca02c'; // GREEN
      var againstColor = '#ff7f0e'; // RED
      var noneColor = '#1f77b4'; // BLUE

      if (typeData === 'Unseen data') {
        if (stance === 'All') {
          //url = 'https://ieccs.herokuapp.com/api/visual/new/organization/' + stance;
          url1 = 'https://ieccs.herokuapp.com/api/visual/new/organization/FAVOR';
          url2 = 'https://ieccs.herokuapp.com/api/visual/new/organization/AGAINST';
          url3 = 'https://ieccs.herokuapp.com/api/visual/new/organization/NONE';
        }
        else if (stance === 'Favor + Against') {
          url1 = 'https://ieccs.herokuapp.com/api/visual/new/organization/FAVOR';
          url2 = 'https://ieccs.herokuapp.com/api/visual/new/organization/AGAINST';
        }
        else {
          url = 'https://ieccs.herokuapp.com/api/visual/new/organization/' + stance.toUpperCase();
        }
      }
      else {
        if (stance === 'All') {
          //url = 'https://ieccs.herokuapp.com/api/visual/old/organization/' + stance;
          url1 = 'https://ieccs.herokuapp.com/api/visual/old/organization/FAVOR';
          url2 = 'https://ieccs.herokuapp.com/api/visual/old/organization/AGAINST';
          url3 = 'https://ieccs.herokuapp.com/api/visual/old/organization/NONE';
        }
        else if (stance === 'Favor + Against') {
          url1 = 'https://ieccs.herokuapp.com/api/visual/old/organization/FAVOR';
          url2 = 'https://ieccs.herokuapp.com/api/visual/old/organization/AGAINST';
        }
        else {
          url = 'https://ieccs.herokuapp.com/api/visual/old/organization/' + stance.toUpperCase();
        }

      }
      if (stance === 'All') {
        var favorData, againstData, noneData = [];

        req1 = $http.get(url1)
          .success(function (info) {
            //console.log('Favor success');
            favorData = setColor(info.Data, favorColor);
          })
          .error(function (err) {
            self.alert(1);
            console.log(err);
          });

        req2 = $http.get(url2)
          .success(function (info) {
            //console.log('against success');
            againstData = setColor(info.Data, againstColor);
          })
          .error(function (err) {
            self.alert(1);
            console.log(err);
          });
        req3 = $http.get(url3)
          .success(function (info) {
            //console.log('none success');
            noneData = setColor(info.Data, noneColor);
          })
          .error(function (err) {
            self.alert(1);
            console.log(err);
          });

        $q.all([req1, req2, req3]).then(function() {
          data = againstData.concat(favorData.concat(noneData));
          data.sort(compare);
          console.log('all requests received and compared');
          updateBar(75, self);
          drawMap(data, typeData, self);
        });
      }
      else if (stance === 'Favor + Against') {
        var fData, aData = [];

        req1 = $http.get(url1)
          .success(function (info) {
            //console.log('Favor success');
            fData = setColor(info.Data, favorColor);
          })
          .error(function (err) {
            self.alert(1);
            console.log(err);
          });

        req2 = $http.get(url2)
          .success(function (info) {
            //console.log('against success');
            aData = setColor(info.Data, againstColor);
          })
          .error(function (err) {
            self.alert(1);
            console.log(err);
          });

        $q.all([req1, req2]).then(function() {
          data = aData.concat(fData);
          data.sort(compare);
          console.log('all requests received and compared');
          updateBar(75, self);
          drawMap(data, typeData, self);
        });
      }
      else {
        req = $http.get(url)
          .success(function (info) {
            console.log('Data retrieved..');
            if (stance === 'Favor') {
              data = setColor(info.Data, favorColor);
            } else if (stance === 'Against') {
              data = setColor(info.Data, againstColor);
            } else {
              data = setColor(info.Data, noneColor);
            }
            updateBar(75, self);
            drawMap(data, typeData, self);
          })
          .error(function (err) {
            self.alert(1);
            console.log(err);
          });
      }
    }

    function init() {
      var self = this;
      self.alert = ko.observable(0);
      self.progress = ko.observable(102);
      self.progressPct = ko.observable('0%');
      self.alertMsg = ko.observable('Error retrieving some of the data!');
      self.allStancesFalse = ko.observable(true);

      self.stanceModel = [
        {id: 0, type:'All', icon: '', status: ko.observable(true)},
        {id: 1, type:'Favor + Against', icon: '', status: ko.observable(false)},
        {id: 2, type:'Favor', icon: '<i class="fa fa-circle background-favor"></i>', status: ko.observable(false)},
        {id: 3, type:'Against', icon: '<i class="fa fa-circle background-against"></i>', status: ko.observable(false)},
        {id: 4, type:'None', icon: '<i class="fa fa-circle background-none"></i>', status: ko.observable(false)}
      ];


      self.updateStanceStatus = function(index, visModel)  {
        console.log('progress = ' + this.progress());
        updateBar(5, self);
        self.stanceModel.forEach(function(item) {
          if (index === item.id) {
            item.status(true);
            console.log('Requesting..');
            updateBar(50, self);
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
      self.progressPct(self.progress() + '%');
      console.log('progress = ' + self.progress());
      console.log('progressMSG = ' + self.progressPct());
    }

    function drawMap(mapData, typeData, self) {
      console.log('Building map');
      updateBar(95, self);
      var latlong = coordinates;
      var minBulletSize = 6;
      var maxBulletSize = 60;
      var min = 1;
      var max = 7000;

      // build map

      window.map = new AmCharts.AmMap();
      AmCharts.theme = AmCharts.themes.dark;

      window.map.addTitle('Author countries', 14);
      window.map.addTitle('from '+typeData, 11);
      window.map.areasSettings = {
        unlistedAreasColor: '#000000',
        unlistedAreasAlpha: 0.5
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

      var codeList = [];
      mapData.forEach(function(item) {
        codeList.push({code: item.code,
          first: false, second:false, last:false,
          check1: false, check2: false});
      });

      var valueDiff = 100;
      mapData.forEach(function(dataItem) {
        var valueTwo = dataItem.value;
        var id = dataItem.code;
          if (valueTwo < valueDiff) {
            codeList.forEach(function (item) {
              if (item.code === id && item.first === false) {
                item.first = true;
              }
              else if (item.code === id && item.second === false) {
                item.second = true;
              }
              else if (item.code === id && item.last === false) {
                item.last = true;
              }
            });
          }
        });

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
        var largest = 11;
        var medium = 8;
        var smallest = 5;
        if (valueTwo < valueDiff) {
          codeList.forEach(function(item) {
            if (item.code === id && item.last) {
              if (!item.check1) {
                size = largest;
                item.check1 = true;
              }
              else if (!item.check2) {
                size = medium;
                item.check2 = true;
              }
              else {
                size = smallest;
              }
            }
            else if (item.code === id && item.second) {
              if (!item.check1) {
                size = medium;
                item.check1 = true;
              }
              else {
                size = smallest;
              }
            }
            else if (item.code === id){
              size = smallest;
            }
          });
        }


        dataProvider.images.push({
          type: 'circle',
          width: size ,
          height: size ,
          color: dataItem.color,
          alpha: 1,
          bringForwardOnHover: false,
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

      setTimeout(function(){
        updateBar(102, self);
      }, 600);
    }


    return {
      viewModel: init,
      template: template
    };

});



