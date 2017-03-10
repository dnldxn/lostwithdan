---
---

{% assign current_lat = site.data.stats.current_location.lat %}
{% assign current_lon = site.data.stats.current_location.lon %}

var map;
var infowindow;

function initMap() {
    var current_location = new google.maps.LatLng({{ current_lat }}, {{ current_lon }});
    var zoomLevel = 8

    /* define map center, zoom level, and basic options */
    map = new google.maps.Map(document.getElementById('googleMap'), {
        center: current_location,
        zoom: zoomLevel,
        mapTypeControl: true,
            mapTypeControlOptions: {
                style: google.maps.MapTypeControlStyle.DROPDOWN_MENU,
                position: google.maps.ControlPosition.TOP_RIGHT,
        },
        streetViewControl: false,
        zoomControl: true
    });

    /* Load coordinates from CSV file and create POI array */
    var coordinates = [
        {% for p in site.data.atdb092116023143ALL %}
            {% if p.lat and p.lon %}
                { nm: "{{p.name}}", loc: {lat: {{p.lat}}, lng: {{p.lon}}} },
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
            position: c.loc,
            map: map,
            icon: smallCircle,
            title: c.nm
        });

        /* Add the POI to a list that we use to draw the line later */
        latLngArray.push(c.loc);
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
        position: current_location,
        map: map,
        title: 'Current Location!',
        icon: {
            url: "/assets/images/hiker_med.png",
            origin: new google.maps.Point(0, 0),
            anchor: new google.maps.Point(25, 40)   /* just a little up from the bottom center (the image is 50 x 62) */
        },
        animation: google.maps.Animation.DROP
    });

    /* Add the list of Post Offices (if any) that have been identified by the build process */
    infowindow = new google.maps.InfoWindow();
    var post_offices = {{ site.data.post_offices | jsonify }}
    
    for (var i = 0; i < post_offices.length; i++) {
        var po = post_offices[i]

        var marker = new google.maps.Marker({
            map: map,
            position: {lat: parseFloat(po.lat), lng: parseFloat(po.lng)},
            icon: {
                url: 'https://maps.gstatic.com/mapfiles/place_api/icons/post_office-71.png',
                scaledSize: new google.maps.Size(20, 20)
            },
            content: "<b><a href='" + po.url + "' target='_blank'>" + po.nm + "</a></b><br />" + po.addr + "<br />" + po.phone
        });

        google.maps.event.addListener(marker, 'click', function() {
            infowindow.setContent(this.content);
            infowindow.open(map, this);
        });
    }

    /* Add button to reset the view to my current location */
    var resetLocationButton = document.getElementById('resetLocationButton')
    resetLocationButton.addEventListener('click', function() {
        map.setCenter(current_location);
        map.setZoom(zoomLevel)
    });
    map.controls[google.maps.ControlPosition.RIGHT_BOTTOM].push(resetLocationButton);
}
