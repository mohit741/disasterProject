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
var navInfos = {
    'food': fh+'food'+sh,
    'water': '',
    'shelter': '',
    'first_aid': '',
    'help': ''
};
function needs() {
    flag = 0;
    console.log(flag);
    //return false;
}
function offers() {
    flag = 1;
    console.log(flag);
    //return false;
}
function initMp() {
    uluru = {lat: 12.9717, lng: 77.594};
    map = new google.maps.Map(document.getElementById('map'), {
        zoom: 4,
        center: uluru
        /*mapTypeId: google.maps.MapTypeId.TERRAIN*/
    });
    // see https://developers.google.com/maps/documentation/javascript/examples/places-searchbox
    var input = document.getElementById('pac-input');
    var searchBox = new google.maps.places.SearchBox(input);
    map.controls[google.maps.ControlPosition.TOP_LEFT].push(input);
    // Bias the SearchBox results towards current map's viewport.
    map.addListener('bounds_changed', function () {
        searchBox.setBounds(map.getBounds());
    });
    markers = [];
    // Listen for the event fired when the user selects a prediction and retrieve
    // more details for that place.
    searchBox.addListener('places_changed', function () {
        var places = searchBox.getPlaces();
        if (places.length == 0) {
            return;
        }
        // Clear out the old markers.
        markers.forEach(function (marker) {
            marker.setMap(null);
        });
        markers = [];
        // For each place, get the icon, name and location.
        var bounds = new google.maps.LatLngBounds();
        places.forEach(function (place) {
            if (!place.geometry) {
                console.log("Returned place contains no geometry");
                return;
            }
            /*var icon = {
             url: place.icon,
             size: new google.maps.Size(71, 71),
             origin: new google.maps.Point(0, 0),
             anchor: new google.maps.Point(17, 34),
             scaledSize: new google.maps.Size(25, 25)
             };*/
            var jumping_marker = new google.maps.Marker({
                map: map,
                title: place.name,
                position: place.geometry.location
            })
            // Create a marker for each place.
            markers.push(jumping_marker);
            jumping_marker.setAnimation(google.maps.Animation.BOUNCE);
            setTimeout(function stopBounce() {
                jumping_marker.setAnimation(null);
            }, 2200);
            var contentString = '<a href="#" onclick="new function(){markers.forEach(function(marker){marker.setMap(null);});}"> Clear markers </a>';
            var infowindow = new google.maps.InfoWindow({
                content: contentString
            });
            jumping_marker.addListener('click', function () {
                infowindow.open(map, jumping_marker);
            });
            if (place.geometry.viewport) {
                // Only geocodes have viewport.
                bounds.union(place.geometry.viewport);
            } else {
                bounds.extend(place.geometry.location);
            }
        });
        map.fitBounds(bounds);
    });
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
$(document).ready(function () {
    $('.list-group-item').click(function () {
        $('.list-group-item').removeClass('active');
        $(this).addClass('active');
    });
});
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
                infoWindow.setContent('Contact : ' + markers[i]['ph'] + '<br><br>Info : ' + markers[i]['info'] + '<br><br><a onclick="deleteMarker(' + marker.id + ')">Processed</a>');
                infoWindow.open(map, marker);
            }
        })(marker, i));

        // Automatically center the map fitting all markers on the screen
        map.fitBounds(bounds);
    }
}