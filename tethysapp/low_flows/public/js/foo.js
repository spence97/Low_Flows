

$(document).ready(function() {

  // Create new Overlay with the #popup element
  var popup = new ol.Overlay({
      element: document.getElementById('popup')
  });

  // Get the Open Layers map object from the Tethys MapView
  var map = TETHYS_MAP_VIEW.getMap();

  // Add the popup overlay to the map
  map.addOverlay(popup);

  // Get the Select Interaction from the Tethys MapView
  var select_interaction = TETHYS_MAP_VIEW.getSelectInteraction();

  var my_callback = function(e) {
     var popup_element = popup.getElement();

     if (e.target.getArray().length > 0) {
         var feature = e.target.item(0);
         var properties = feature.getProperties();
         var feature_id = properties['feature_id'];
         console.log(feature_id);

         $.ajax({
             url: '/apps/low-flows/rest/bar/',
             data: {
                 'feature_id': feature_id
             }
         }).done(function(data) {
             console.log(data);
              // Get coordinates of the point to set position of the popup
              var coordinates = feature.getGeometry().getCoordinates();
              var lat = feature.get('lat');
              var lon = feature.get('lon');
              coordinates = ol.proj.transform([lon, lat], 'EPSG:4326','EPSG:3857');

              var stats_method = $('#stats_select option:selected').val();


              var popup_content = '<div class="stream-popup">' +
                                      '<p><b>' + 'COMID:' + feature_id + '</b></p>' +
                                      '<table class="table  table-condensed">' +
                                      '</table>' +
                                      '<a href="/apps/low-flows/forecast/?comid=' + feature_id + '&stats_method=' + stats_method + '" class="btn btn-success">View Forecast</a>' +
                                  '</div>';

              // Clean up last popup and reinitialize
              $(popup_element).popover('destroy');

              // Delay arbitrarily to wait for previous popover to
              // be deleted before showing new popover.
              setTimeout(function() {
                  popup.setPosition(coordinates);

                  $(popup_element).popover({
                    'placement': 'top',
                    'animation': true,
                    'html': true,
                    'content': popup_content
                  });

                  $(popup_element).popover('show');
              }, 500);
         });
     } else {
          // remove pop up when selecting nothing on the map
          $(popup_element).popover('destroy');
     }
  };

  // When selected, call function to display properties
  select_interaction.getFeatures().on('change:length', my_callback);

  //TETHYS_MAP_VIEW.onSelectionChange(my_callback);

  // Style functions
  function x7q10_styler(feature, resolution) {
    // get the 7q10 property
    var x7q10 = feature.getProperties()['x7q10'];
    var q = feature.getProperties()['min_forecast_flow'];
    var style;

    // assign style based on property
    if (q > x7q10) {
      style = new ol.style.Style({
        stroke: new ol.style.Stroke({
          color: '#598bdb',
          width: 3
        })
      });

    } else {
      style = new ol.style.Style({
        stroke: new ol.style.Stroke({
          color: 'red',
          width: 3
        })
      });
    }
    
    return style;
  }

    function x7q2_styler(feature, resolution) {
    // get the 7q10 property
    var x7q2 = feature.getProperties()['x7q2'];
    var q = feature.getProperties()['min_forecast_flow'];
    var style;

    // assign style based on property
    if (q > x7q2) {
      style = new ol.style.Style({
        stroke: new ol.style.Stroke({
          color: '#598bdb',
          width: 3
        })
      });

    } else {
      style = new ol.style.Style({
        stroke: new ol.style.Stroke({
          color: 'red',
          width: 3
        })
      });
    }
    
    return style;
  }

    function perc5_styler(feature, resolution) {
    // get the perc5 property
    var perc5 = feature.getProperties()['perc5'];
    var q = feature.getProperties()['min_forecast_flow'];
    var style;

    // assign style based on property
    if (q > perc5) {
      style = new ol.style.Style({
        stroke: new ol.style.Stroke({
          color: '#598bdb',
          width: 3
        })
      });

    } else {
      style = new ol.style.Style({
        stroke: new ol.style.Stroke({
          color: 'red',
          width: 3
        })
      });
    }
    
    return style;
  }

    function perc25_styler(feature, resolution) {
    // get the perc25 property
    var perc25 = feature.getProperties()['perc25'];
    var q = feature.getProperties()['min_forecast_flow'];
    var style;

    // assign style based on property
    if (q > perc25) {
      style = new ol.style.Style({
        stroke: new ol.style.Stroke({
          color: '#598bdb',
          width: 3
        })
      });

    } else {
      style = new ol.style.Style({
        stroke: new ol.style.Stroke({
          color: 'red',
          width: 3
        })
      });
    }
    
    return style;
  }

  // Handle select boxes
  $("#watershedselect").on('change', function(e){
    var value = e.target.value;
    var ol_map = TETHYS_MAP_VIEW.getMap();
    var layers = ol_map.getLayers();
    console.log(layers);
    console.log(value);

    // Turn off all layers
    for (var i = 0; i < layers.getLength(); i++) {
      var layer = layers.item(i);
      if (i > 0) {
        layer.setVisible(false);
      }
    }

    // Turn on selected layer
    if (value == 'SipseyFork') {
      layers.item(1).setVisible(true);
      layers.item(2).setVisible(true);
      layers.item(3).setVisible(true);
      var extent = [-87.54848478610077,34.26079110801598,-87.31337829591592,34.43565709434446]
      TETHYS_MAP_VIEW.zoomToExtent(extent)
    }
    if (value == 'SantaYnez') {
      layers.item(4).setVisible(true);
      layers.item(5).setVisible(true);
      layers.item(6).setVisible(true);
      var extent = [-120.4813637119601,34.463261694407215,-119.42287030829114,34.81338123957116]
      TETHYS_MAP_VIEW.zoomToExtent(extent)
    }
    if (value == 'DeerCreek') {
      layers.item(7).setVisible(true);
      layers.item(8).setVisible(true);
      layers.item(9).setVisible(true);
      var extent = [-121.9542639743601,40.00363165277552,-121.34115598500073,40.36926893570012]
      TETHYS_MAP_VIEW.zoomToExtent(extent)
    }
    if (value == 'NHD') {
      layers.item(10).setVisible(true);
      var extent = [-124.70777731699997,24.88423195100006,-66.98839640599996,52.862568329000055]
      TETHYS_MAP_VIEW.zoomToExtent(extent)
    }

  });

  // Stats select
  $('#stats_select').on('change', function(e) {
      var value = e.target.value;
      var map = TETHYS_MAP_VIEW.getMap();
      var layers = map.getLayers();

      console.log(layers);
      console.log(value);
      
      if (value == '7Q10') {
        // Change set 7q10 styling function
        layers.item(3).setStyle(x7q10_styler);
        layers.item(6).setStyle(x7q10_styler);
        layers.item(9).setStyle(x7q10_styler);

      } else if (value == '7Q2') {
        // Change set 7q2 styling function
        layers.item(3).setStyle(x7q2_styler);
        layers.item(6).setStyle(x7q2_styler);
        layers.item(9).setStyle(x7q2_styler);

      } else if (value == 'Perc5') {
        // Change set 7q2 styling function
        layers.item(3).setStyle(perc5_styler);
        layers.item(6).setStyle(perc5_styler);
        layers.item(9).setStyle(perc5_styler);

      }else if (value == 'Perc25') {
        // Change set 7q2 styling function
        layers.item(3).setStyle(perc25_styler);
        layers.item(6).setStyle(perc25_styler);
        layers.item(9).setStyle(perc25_styler);

      } else {
        // Change set 7q10 styling function
        layers.item(3).setStyle(undefined);
        layers.item(6).setStyle(undefined);
        layers.item(9).setStyle(undefined);
      }

  });
});

