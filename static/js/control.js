/**
 * Created by mohit on 25-01-2019.
 */
/* Flag to determine resource availability need/offer
 0 : needs, 1 : offers
 */

var flag = 0;
var infoWindow, map = null;
var latitude, longitude;
var currentId = 0;
var marks = {};
var uniqueId = function () {
    return ++currentId;
};
function needs() {
    closeNav();
    $('#help').show();
    deleteAll();
    flag = 0;
    console.log(flag);
    //return false;
}
function offers() {
    closeNav();
    $('#help').hide();
    deleteAll();
    flag = 1;
    console.log(flag);
    //return false;
}

function init() {
    $(document).ready(function () {
        $('#load').show();
        $.ajax({
            url: global_url,
            data: {},
            dataType: 'json',
            success: function (data) {
                $('#load').hide();
                latitude = data['lat'];
                longitude = data['lon'];
                initMap(data['lat'], data['lon']);
            }
        });
    });
}
function initMap(lat, lng) {

    $('#load').hide();
    map = new google.maps.Map(
        document.getElementById('map'), {
            zoom: 13, mapTypeId: 'terrain', center: {lat: lat, lng: lng},
            styles: [
                {
                    featureType: "poi",
                    elementType: "labels",
                    stylers: [
                        {
                            visibility: "off"
                        }
                    ]
                }
            ]
        });
    infoWindow = new google.maps.InfoWindow();
}

function openNav(str) {
    document.getElementById("mySidenav").style.width = "15%";
    document.getElementById("infotxt").innerHTML = fh + str + sh;
    document.getElementById("infohead").innerHTML = '  '+str.charAt(0).toUpperCase() + str.substr(1);
    document.getElementById("infoimg").src = urls[str];
    console.log(flag);
    if (map != null)
        initMap(latitude, longitude);
    getMarkers(str);
}
function closeNav() {
    document.getElementById("mySidenav").style.width = "0";
}
/*$(document).ready(function () {
    $('.list-group-item').click(function () {
        $('.list-group-item').removeClass('active');
        $(this).addClass('active');
    });
});*/
function get_hospitals() {
    initMap(latitude, longitude);
    var service = new google.maps.places.PlacesService(map);
    service.nearbySearch({
        location: {lat: latitude, lng: longitude},
        radius: 10000,
        type: ['hospital']
    }, callback);

}
function callback(results, status) {
    if (status === google.maps.places.PlacesServiceStatus.OK) {
        for (var i = 0; i < results.length; i++) {
            createMarker(results[i]);
        }
    }
}

function createMarker(place) {
    var placeLoc = place.geometry.location;
    var marker = new google.maps.Marker({
        map: map,
        position: placeLoc,
        icon: urls['hospital']
    });

    google.maps.event.addListener(marker, 'click', function () {
        infoWindow.setContent(place.name);
        infoWindow.open(map, this);
    });
}
function deleteMarker(id) {
    var marker = marks[id]; // find the marker by given id
    marker.setMap(null);
}
function deleteAll()
{
    for(var key in marks) {
        deleteMarker(key);
    }
}
function getMarkers(type) {
    var mode;
    if (flag == 0)
        mode = 'needs';
    else
        mode = 'offers';
    $(document).ready(function () {
        $('#load').show();
        $.ajax({
            url: mode_url,
            data: {
                'type': type,
                'mode': mode
            },
            dataType: 'json',
            success: function (data) {
                var markers = data['results'];
                console.log(markers);
                setMarkers(markers, type);
            }
        });
    });

}

function setMarkers(markers, type) {
    var bounds = new google.maps.LatLngBounds();
    var i;
    for (i = 0; i < markers.length; i++) {
        var id = uniqueId();
        var position = new google.maps.LatLng(parseFloat(markers[i]['lat']), parseFloat(markers[i]['lon']));
        bounds.extend(position);
        marker = new google.maps.Marker({
            id: id,
            position: position,
            map: map,
            icon: urls[type]
        });
        marks[id] = marker;
        // Allow each marker to have an info window
        google.maps.event.addListener(marker, 'click', (function (marker, i) {
            return function () {
                infoWindow.setContent('Contact : ' + markers[i]['ph'] + '<br><br>Info : ' + markers[i]['info'] + '<br><br><a class="btn btn-success" onclick="deleteMarker(' + marker.id + ')">Processed</a>');
                infoWindow.open(map, marker);
            }
        })(marker, i));

        // Automatically center the map fitting all markers on the screen
        map.fitBounds(bounds);
    }
}