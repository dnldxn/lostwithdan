var map;

function initMap() {

    var bounds = new google.maps.LatLngBounds();

    map = new google.maps.Map(document.getElementById('googleMap'), {
        // center: {lat: 40.2, lng: -78.1093641},
        // zoom: 6,
        mapTypeControl: true,
            mapTypeControlOptions: {
            style: google.maps.MapTypeControlStyle.DROPDOWN_MENU,
            position: google.maps.ControlPosition.TOP_RIGHT
        },
        streetViewControl: false
    });

    // Load coordinates from CSV file and convert to JSON structure
    var coordinates = {{ site.data.atdb092116023143ALL | where_exp: "p", "p.type != 'TOWN'" | where_exp: "p", "p.type != 'HOSTEL'" | jsonify }};
    var latLngArray = new Array();

    var smallCircle = {
        path: 'M -1 0 A 1 1, 0, 0, 0, 1 0 A 1 1, 0, 1, 0, -1 0',
        fillColor: 'mediumslateblue',
        fillOpacity: 0.3,
        scale: 4,
        strokeWeight: 0
    };

    for (var i = 0; i < coordinates.length; i++ ) {
        var c = coordinates[i]
        
        if( c.lat && c.lon ) {
            // Mark the POI on the map with a red dot
            var position = new google.maps.LatLng(c.lat, c.lon);
            bounds.extend(position);
            marker = new google.maps.Marker({
                position: position,
                map: map,
                icon: smallCircle,
                title: c.name //,
                //animation: google.maps.Animation.DROP
            });

            // Add the POI to a list that we use to draw the line later
            latLngArray.push(position);

            // Add a point for the current location (where am I now)
            if(c.dt_reached && !coordinates[i+1].dt_reached) {
                var currentLocation = new google.maps.Marker({
                    position: position,
                    map: map,
                    title: 'Current Location!',
                    icon: {
                        url: "/img/hiker_med.png",
                        origin: new google.maps.Point(0, 0),
                        anchor: new google.maps.Point(25, 40),  // just a little up from the bottom center (the image is 50 x 62)
                    },
                    animation: google.maps.Animation.DROP
                });
            }
        }
    }

    // Automatically center the map fitting all markers on the screen
    map.fitBounds(bounds);

    // Draw a line over all of the points
    var trailPath = new google.maps.Polyline({
        path: latLngArray,
        geodesic: true,
        strokeColor: 'mediumslateblue',
        strokeOpacity: 0.6,
        strokeWeight: 6
    });
    trailPath.setMap(map);
}
