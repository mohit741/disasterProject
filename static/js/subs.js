/**
 * Created by mohit on 16-01-2019.
 */

var lat_input_selector = '#lat',
    lon_input_selector = '#lon';


// If we don't have a lat/lon in the input fields,
// this is where the map will be centered initially.
var initial_lat = 27,
    initial_lon = 82;

// Initial zoom level for the map.
var initial_zoom = 4.5;

var geocoder, map, marker, $lat, $lon;

/**
 * Create HTML elements, display map, set up event listenerss.
 */
function initMap() {
    //$lat = document.getElementById("lat");//$(lat_input_selector);
    // $lon = document.getElementById("lon");//$(lon_input_selector);

    map = new google.maps.Map(
        document.getElementById('locator'), {zoom: 4.5, mapTypeId: 'terrain'});

    geocoder = new google.maps.Geocoder();
    var country = 'India';
    geocoder.geocode({'address': country}, function (results, status) {
        if (status == google.maps.GeocoderStatus.OK) {
            map.setCenter(results[0].geometry.location);
        }
    });
    marker = new google.maps.Marker({
        map: map,
        draggable: true
    });

    //if (has_initial_loc) {
    setMarkerPosition(initial_lat, initial_lon);
    //}

    google.maps.event.addListener(map, 'click', function (ev) {
        setMarkerPosition(ev.latLng.lat(), ev.latLng.lng());
    });

    google.maps.event.addListener(marker, 'dragend', function () {
        setInputValues(marker.getPosition().lat(), marker.getPosition().lng());
    });
}

/**
 * Re-position marker and set input values.
 */
function setMarkerPosition(lat, lon) {
    marker.setPosition({lat: lat, lng: lon});
    setInputValues(lat, lon);
}

/**
 * Set the values of all the input fields, including getting the
 * geocoded data for address and country, based on lat and lon.
 */
function setInputValues(lat, lon) {
    var x = Math.round( lat * 1e5 )/1e5;
    var y = Math.round( lon * 1e5 )/1e5;
    document.getElementById('lat').value = x;
    document.getElementById('lon').value = y;
}

/**
 * Set the value of $input to val, with the correct decimal places.
 * We work out decimal places using the <input>'s step value, if any.
 */
/* function setLatLonInputValue($input, val) {
 // step should be like "0.000001".
 var step = $input.prop('step');
 var dec_places = 0;

 if (step) {
 if (step.split('.').length == 2) {
 dec_places = step.split('.')[1].length;
 }

 val = val.toFixed(dec_places);
 }

 $input.val(val);
 }*/