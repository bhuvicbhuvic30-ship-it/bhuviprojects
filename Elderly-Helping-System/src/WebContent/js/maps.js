function initMap() {
    navigator.geolocation.getCurrentPosition(function(position) {

        const location = {
            lat: position.coords.latitude,
            lng: position.coords.longitude
        };

        const map = new google.maps.Map(document.getElementById("map"), {
            zoom: 15,
            center: location,
        });

        new google.maps.Marker({
            position: location,
            map: map
        });

    });
}
