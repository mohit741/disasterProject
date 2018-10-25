/**
 * Created by HP on 10/18/2018.
 */
var map;
var marker;
var markerOpacity = markerOpacityIncrement = 0.05;
function initMap() {
    map = new google.maps.Map(
        document.getElementById('india_flood_map'), {zoom: 4.5, mapTypeId: 'terrain'});
    var geocoder = new google.maps.Geocoder();
    var country = 'India';
    geocoder.geocode( {'address' : country}, function(results, status) {
        if (status == google.maps.GeocoderStatus.OK) {
            map.setCenter(results[0].geometry.location);
                        }
    });
    marker = new google.maps.Marker({
          map: map,
          draggable: false,
          position: {lat: 27, lng: 84}
        });
    marker.setOpacity(0);
    setTimeout(function() {
        fadeInMarkers(marker);
    }, 100);
    marker.setAnimation(google.maps.Animation.BOUNCE);
}
var fadeInMarkers = function(marker) {

    if (markerOpacity <= 1) {

            marker.setOpacity(markerOpacity);

        // increment opacity
        markerOpacity += markerOpacityIncrement;

        // call this method again
        setTimeout(function() {
            fadeInMarkers(marker);
        }, 50);

    } else {
        markerOpacity = markerOpacityIncrement; // reset for next use
    }
};

function getCircle() {
        return {
          path: google.maps.SymbolPath.CIRCLE,
          fillColor: 'red',
          fillOpacity: 0.7,
          scale: 30,
          strokeColor: 'white',
          strokeWeight: .5
        };
      }