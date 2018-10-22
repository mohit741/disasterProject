/**
 * Created by HP on 10/18/2018.
 */
var map;
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
    map.data.addGeoJson(zones);
    map.data.setStyle(function(feature) {
        var magnitude = feature.getProperty('deaths');
        return {
            icon: getCircle(magnitude)
        };
    });
    map.data.addListener('click',function(event){
          window.location.href = window.location.href+"states/"+event.feature.getProperty('name');
    });
}
function getCircle(magnitude) {
        return {
          path: google.maps.SymbolPath.CIRCLE,
          fillColor: 'red',
          fillOpacity: Math.pow((Math.log(magnitude)/10),2) * 1.50,
          scale: 30,
          strokeColor: 'white',
          strokeWeight: .5
        };
      }