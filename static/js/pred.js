/**
 * Created by HP on 10/18/2018.
 */
var map,heatmap;
var marker;

// Get data
function init() {
    $(document).ready(function(){
        //$('#load').show();
        $.ajax({
        url: global_url,
        data: {
        },
        dataType: 'json',
        success: function (data) {
            //$('#load').hide();
            //console.log(data);
            var arr = [];
            for(var key in data)
            {
                arr.push(new google.maps.LatLng(data[key][1], data[key][0]));
            }
            //console.log(arr);
            initMap(arr);
        }
      });
    });
}
// Initialize Map
function initMap(data) {
    map = new google.maps.Map(
        document.getElementById('india_flood_map'), {zoom: 4.5, mapTypeId: 'satellite'});
    var geocoder = new google.maps.Geocoder();
    var country = 'India';
    var infoWindow = new google.maps.InfoWindow(),i;
    geocoder.geocode({'address': country}, function (results, status) {
        if (status == google.maps.GeocoderStatus.OK) {
            map.setCenter(results[0].geometry.location);
        }
    });
    heatmap = new google.maps.visualization.HeatmapLayer({
          data: data,
          map: map,
          radius: 5
        });
    var gradient = [
          'rgba(0, 255, 255, 0)',
          'rgba(0, 255, 255, 1)',
          'rgba(0, 191, 255, 1)',
          'rgba(0, 127, 255, 1)',
          'rgba(0, 63, 255, 1)',
          'rgba(0, 0, 255, 1)',
          'rgba(0, 0, 223, 1)',
          'rgba(0, 0, 191, 1)',
          'rgba(0, 0, 159, 1)',
          'rgba(0, 0, 127, 1)',
          'rgba(63, 0, 91, 1)',
          'rgba(127, 0, 63, 1)',
          'rgba(191, 0, 31, 1)',
          'rgba(255, 0, 0, 1)'
        ];
        heatmap.set('gradient', heatmap.get('gradient') ? null : gradient);
}
