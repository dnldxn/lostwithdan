var map;

function initMap() {

    var bounds = new google.maps.LatLngBounds();

    map = new google.maps.Map(document.getElementById('googleMap'), {
        mapTypeControl: true,
            mapTypeControlOptions: {
            style: google.maps.MapTypeControlStyle.DROPDOWN_MENU,
            position: google.maps.ControlPosition.TOP_RIGHT
        },
        streetViewControl: false
    });

    // Load coordinates from CSV file and convert to JSON structure
    var coordinates = {{ site.data.atdb092116023143ALL | jsonify }};
    var latLngArray = new Array();

    for (var i = 0; i < coordinates.length; i++ ) {
        var c = coordinates[i]
        
        if( ["FEATURE","SHELTER"].indexOf(c.type) > -1 && c.lat && c.lon ) {
            //console.log(i + ", " + c.type + ", " + c.name + ", " + c.lat + ", " + c.lon)

            var position = new google.maps.LatLng(c.lat, c.lon);
            bounds.extend(position);
            marker = new google.maps.Marker({
                position: position,
                map: map,
                title: c.name
            });

            // Automatically center the map fitting all markers on the screen
            map.fitBounds(bounds);

            latLngArray.push(position);
        }
    }

    // Draw a line over all of the points
    var trailPath = new google.maps.Polyline({
        path: latLngArray,
        geodesic: true,
        strokeColor: '#FF0000',
        strokeOpacity: 0.6,
        strokeWeight: 6
    });
    trailPath.setMap(map);
}
