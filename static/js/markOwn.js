/**
 * Created by mohit on 16-01-2019.
 */

var res='';
var geocoder, map, marker;
/**
 * Create HTML elements, display map, set up event listenerss.
 */
function initMap() {
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

    setMarkerPosition(27, 82);
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

    setInputValues(lat, lon);
    $(document).ready(function(){
        $('#load').show();
        $.ajax({
        url: global_url,
        data: {
          'lon': lon, 'lat': lat
        },
        dataType: 'json',
        success: function (data) {
            geocodeLatLng(lat,lon);
            //console.log(res);
            $('#load').hide();
            document.getElementById('tweet').innerHTML =  data['tweets'];

        }
      });
    });
    marker.setPosition({lat: lat, lng: lon});
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

function geocodeLatLng(lat,lng) {
        var latlng = {lat: lat, lng: lng};
        //console.log(latlng);
        geocoder.geocode({'location': latlng}, function(results, status) {
          if (status === 'OK') {
            if (results[0]) {
                 var i = 0;
                 res = results[0].formatted_address;
                 while(res[i]!=',') i++;
                 res = res.slice(i+1,res.length-7);
                 res = res.replace(/[0-9]/g, '');
                 document.getElementById('loc').innerHTML =  res;
                 console.log(res);
            } else {
              window.alert('No results found');
            }
          } else {
            window.alert('Geocoder failed due to: ' + status);
          }
        });
        //console.log(res);
      }

function saveLoc()
{
    $(document).ready(function(){
        $.ajax({
        url: save_url,
        data: {
          'lon': Math.round( marker.getPosition().lng() * 1e5 )/1e5, 'lat': Math.round( marker.getPosition().lat() * 1e5 )/1e5
        },
        dataType: 'json',
        success: function (data) {
            $('#save').html('Saved !');
        }
      });
    });
}