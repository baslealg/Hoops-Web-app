function initMap() {

    const gamesMap = new google.maps.Map(document.querySelector('#games-map'), {
      center: {lat: 37.0902, lng: -95.7129}, 
    zoom: 4
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