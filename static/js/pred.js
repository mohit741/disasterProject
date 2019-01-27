/**
 * Created by HP on 10/18/2018.
 */
var map;
var marker;
var markerOpacity = markerOpacityIncrement = 0.05;

// Get data
function init() {
    $(document).ready(function(){
       // $('#load').show();
        $.ajax({
        url: global_url,
        data: {
        },
        dataType: 'json',
        success: function (data) {
            initMap(data);
        }
      });
    });
}
// Initialize Map
function initMap(markers) {
    map = new google.maps.Map(
        document.getElementById('india_flood_map'), {zoom: 4.5, mapTypeId: 'terrain'});
    var bounds = new google.maps.LatLngBounds();
    var geocoder = new google.maps.Geocoder();
    var country = 'India';
    var infoWindow = new google.maps.InfoWindow(),i;
    geocoder.geocode({'address': country}, function (results, status) {
        if (status == google.maps.GeocoderStatus.OK) {
            map.setCenter(results[0].geometry.location);
        }
    });
    for (i = 0; i < markers.length; i++) {
        var position = new google.maps.LatLng(markers[i][1], markers[i][2]);
        bounds.extend(position);
        marker = new google.maps.Marker({
            map: map,
            draggable: false,
            position: position
        });
        marker.setOpacity(0);
        setTimeout(function () {
            fadeInMarkers(marker);
        }, 100);
        marker.setAnimation(google.maps.Animation.BOUNCE);
        // Allow each marker to have an info window
        google.maps.event.addListener(marker, 'click', (function (marker, i) {
            return function () {
                infoWindow.setContent(infoWindowContent[i][0]);
                infoWindow.open(map, marker);
            }
        })(marker, i));

        // Automatically center the map fitting all markers on the screen
        map.fitBounds(bounds);
    }
}
var fadeInMarkers = function (marker) {

    if (markerOpacity <= 1) {

        marker.setOpacity(markerOpacity);

        // increment opacity
        markerOpacity += markerOpacityIncrement;

        // call this method again
        setTimeout(function () {
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