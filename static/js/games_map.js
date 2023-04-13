function initMap() {

    let geocoder = new google.maps.Geocoder();
    let zip_addy = "10001";
    geocoder.geocode({ 'address': zip_addy }, function(results, status) {
    if (status == 'OK') {
      let latitude = results[0].geometry.location.lat();
      let longitude = results[0].geometry.location.lng();
      let gamesMap = new google.maps.Map(document.getElementById('games-map'), {
        zoom: 10,
        center: {lat: latitude, lng: longitude}
    });
  } else {
    alert('Geocode was not successful for the following reason: ' + status);
  }
});
    fetch('/api/locations')
    .then(response => response.json())
    .then(data => {
      console.log(data);  
      data.forEach(location => {
        const marker = new google.maps.Marker({
          position: { lat: parseFloat(location.latitude), lng: parseFloat(location.longitude) },
          map: gamesMap,
          title: location.latitude,
        });
      });
    })
  }