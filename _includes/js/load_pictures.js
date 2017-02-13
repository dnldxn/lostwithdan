// main photo: //c1.staticflickr.com/3/2101/32721982582_e8e78dd402_k.jpg
// lightbox url: https://www.flickr.com/photos/131617024@N05/32834509166/in/album-72157680188533126/lightbox/
// href: /photos/131617024@N05/32031737834/in/album-72157680188533126/
// share link: https://www.flickr.com/gp/131617024@N05/704Beh

var xmlhttp = new XMLHttpRequest();

// Build API Url
var url = "https://api.flickr.com/services/rest/?method=flickr.photosets.getPhotos"
url += "&format=json&nojsoncallback=1"
url += "&api_key=f17639e3d18eca2dea2f321aaf3e2e84"
url += "&photoset_id=72157680188533126"
url += "&user_id=131617024%40N05"

// console.log(url)


function buildThumbnailUrl(photo) {
    return 'https://farm' + photo.farm + '.staticflickr.com/' + photo.server +
        '/' + photo.id + '_' + photo.secret + '_q.jpg';
}

function buildPhotoUrl(photo) {
    return 'https://farm' + photo.farm + '.staticflickr.com/' + photo.server +
        '/' + photo.id + '_' + photo.secret + '.jpg';
}

function buildPhotoLargeUrl(photo) {
    return 'https://farm' + photo.farm + '.staticflickr.com/' + photo.server +
        '/' + photo.id + '_' + photo.secret + '_b.jpg';
}

function buildLightBoxUrl(photo) {
    return 'https://www.flickr.com/photos/131617024@N05/' + photo.id + '/in/album-72157680188533126/lightbox/';
}


xmlhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
        var myArr = JSON.parse(this.responseText);
        myFunction(myArr);
    }
};

xmlhttp.open("GET", url, true);
xmlhttp.send();

function myFunction(arr) {
    // console.log(arr)

    // extract the photo list
    var photos = arr.photoset.photo
    
    // loop over all the photos and generate html image links for the gallery
    var out = "";
    var i;
    for(i = 0; i < photos.length; i++) {
        var small = buildPhotoUrl(photos[i])
        var full = buildLightBoxUrl(photos[i])

        out += '<a href="'+ full + '"><img src="'+ small + '" alt="" /></a>'
    }
    document.getElementById("photo-gallery").innerHTML = out;
}
