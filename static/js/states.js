/**
 * Created by HP on 10/19/2018.
 */
var map1,map2;
var icon = {url : 'https://upload.wikimedia.org/wikipedia/commons/8/85/Dam.svg', scaledSize: new google.maps.Size(5, 5)};
function initialize()
{
    initMap1();
}
function initMap1()
{
    map1 = new google.maps.Map(
        document.getElementById('dam_map'), {zoom: 7, mapTypeId: 'terrain'});
    var geocoder = new google.maps.Geocoder();
    geocoder.geocode( {'address' : state}, function(results, status) {
        if (status == google.maps.GeocoderStatus.OK) {
            map1.setCenter(results[0].geometry.location);
                        }
    });
    map1.data.addGeoJson(stations);
    map1.data.setStyle(function(feature) {
        return {
            icon: icon,
            optimized: false
        };
    });
    var infowindow = new google.maps.InfoWindow();
    map1.data.addListener('click', function(event) {
	    var myHTML = event.feature.getProperty("name");
        var code = event.feature.getProperty("code");
	    infowindow.setContent("<a href='"+window.location.href+"/"+code+"'style='width:150px; font-size:20px;'>"+myHTML+"</a>");
	// position the infowindow on the marker
	    infowindow.setPosition(event.feature.getGeometry().get());
	// anchor the infowindow on the marker
	    infowindow.setOptions({pixelOffset: new google.maps.Size(0,-30)});
	    infowindow.open(map1);
    });
}