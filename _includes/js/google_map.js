{% assign current_lat = site.data.stats.current_location.lat %}
{% assign current_lon = site.data.stats.current_location.lon %}

var map;

function initMap() {

    /* define map center, zoom level, and basic options */
    map = new google.maps.Map(document.getElementById('googleMap'), {
        center: { lat: {{current_lat}}, lng: {{current_lon}} },
        zoom: 8,
        mapTypeControl: true,
            mapTypeControlOptions: {
            style: google.maps.MapTypeControlStyle.DROPDOWN_MENU,
            position: google.maps.ControlPosition.TOP_RIGHT
        },
        streetViewControl: false
    });

    /* Load coordinates from CSV file and create POI array */
    var coordinates = [
        {% for p in site.data.atdb092116023143ALL %}
            {% if p.type == 'SHELTER' or p.type == 'FEATURE' %}
                {% if p.lat and p.lon %}
                    { name: "{{p.name}}", position: new google.maps.LatLng( {{p.lat}}, {{p.lon}} ) },
                {% endif %}
            {% endif %}
        {% endfor %}
    ]
    var latLngArray = Array();

    /* Define small blue dot */
    var smallCircle = {
        path: 'M -1 0 A 1 1, 0, 0, 0, 1 0 A 1 1, 0, 1, 0, -1 0',
        fillColor: 'mediumslateblue',
        fillOpacity: 0.3,
        scale: 4,
        strokeWeight: 0
    };

    /* Draw a blue dot at every POI */
    for (var i = 0; i < coordinates.length; i++ ) {
        var c = coordinates[i]
        
        marker = new google.maps.Marker({
            position: c.position,
            map: map,
            icon: smallCircle,
            title: c.name
        });

        /* Add the POI to a list that we use to draw the line later */
        latLngArray.push(c.position);
    }

    /* Draw a line over all of the points */
    var trailPath = new google.maps.Polyline({
        path: latLngArray,
        geodesic: true,
        strokeColor: 'mediumslateblue',
        strokeOpacity: 0.6,
        strokeWeight: 6
    });
    trailPath.setMap(map);

    /* Add a point for the current location (where am I now) */
    var currentLocation = new google.maps.Marker({
        position: { lat: {{current_lat}}, lng: {{current_lon}} },
        map: map,
        title: 'Current Location!',
        icon: {
            url: "/img/hiker_med.png",
            origin: new google.maps.Point(0, 0),
            anchor: new google.maps.Point(25, 40),   /* just a little up from the bottom center (the image is 50 x 62) */
        },
        animation: google.maps.Animation.DROP
    });
}
