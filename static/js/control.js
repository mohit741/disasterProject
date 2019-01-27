/**
 * Created by mohit on 25-01-2019.
 */
/* Flag to determine resource availability need/offer
 0 : needs, 1 : offers, 2 : hospitals, 3 : report
 */
var flag = 0;
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
    marker = new google.maps.Marker({
        map: map,
        draggable: true
    });
    //setMarkerPosition(lat, lng);
}

function openNav(str) {
    document.getElementById("mySidenav").style.width = "15%";
    document.getElementById("infotxt").innerHTML = str;
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

rescueMarkers = [];
rescueRequests = [{lat: -25.363, lng: 131.044}, {lat: -20.303, lng: 156.044}];
function rescueHandle(checkBox) {
    if (checkBox.checked) {
        for (var i = 0; i < rescueRequests.length; i++) {
            rescueMarkers.push(new google.maps.Marker({
                position: rescueRequests[i],
                map: map,
                icon: 'http://chart.apis.google.com/chart?chst=d_map_pin_letter&chld=%E2%80%A2|F00'
            }));
        }
    }
    else {
        for (var i = 0; i < rescueMarkers.length; i++) {
            rescueMarkers[i].setMap(null);
        }
    }
}
waterMarkers = [];
waterRequests = [{lat: 12.971, lng: 77.594}, {lat: 12.839, lng: 76.988}, {lat: 12.456, lng: 77.236}];
function waterHandle(checkBox) {
    if (checkBox.checked) {
        for (var i = 0; i < waterRequests.length; i++) {
            waterMarkers.push(new google.maps.Marker({
                position: waterRequests[i],
                map: map,
                icon: 'http://chart.apis.google.com/chart?chst=d_map_pin_letter&chld=%E2%80%A2|0FF'
            }));
        }
    }
    else {
        for (var i = 0; i < waterMarkers.length; i++) {
            waterMarkers[i].setMap(null);
        }
    }
}
foodMarkers = [];
foodRequests = [{lat: -15.363, lng: 122.044}, {lat: -25.303, lng: 120.044}];
function foodHandle(checkBox) {
    if (checkBox.checked) {
        for (var i = 0; i < foodRequests.length; i++) {
            foodMarkers.push(new google.maps.Marker({
                position: foodRequests[i],
                map: map,
                icon: 'http://chart.apis.google.com/chart?chst=d_map_pin_letter&chld=%E2%80%A2|0F0'
            }));
        }
    }
    else {
        for (var i = 0; i < foodMarkers.length; i++) {
            foodMarkers[i].setMap(null);
        }
    }
}
function setMarkers(type) {
    $(document).ready(function () {
        $('#load').show();
        $.ajax({
            url: global_url,
            data: {
                'lon': lon, 'lat': lat
            },
            dataType: 'json',
            success: function (data) {
                geocodeLatLng(lat, lon);
                //console.log(res);
                $('#load').hide();
                document.getElementById('tweet').innerHTML = data['tweets'];
                marker.setPosition({lat: lat, lng: lon});
            }
        });
    });
}