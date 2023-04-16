function initMap() {
  let zipcode;
    fetch('/api/zipcode')
  .then(response => response.json())
  .then(data => {
     zipcode = data.zipcode
    console.log(data.zipcode.toString())
    let geocoder = new google.maps.Geocoder();
  let gamesMap;

let zip_addy = zipcode.toString();
geocoder.geocode({ 'address': zip_addy }, function(results, status) {
  if (status == 'OK') {
    let latitude = results[0].geometry.location.lat();
    let longitude = results[0].geometry.location.lng();
    gamesMap = new google.maps.Map(document.getElementById('games-map'), {
      zoom: 10,
      center: {lat: latitude, lng: longitude}
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
  } else {
    alert('Geocode was not successful for the following reason: ' + status);
  }
});
  });
//   let geocoder = new google.maps.Geocoder();
//   let gamesMap;

// let zip_addy = zipcode.toString();
// geocoder.geocode({ 'address': zip_addy }, function(results, status) {
//   if (status == 'OK') {
//     let latitude = results[0].geometry.location.lat();
//     let longitude = results[0].geometry.location.lng();
//     gamesMap = new google.maps.Map(document.getElementById('games-map'), {
//       zoom: 10,
//       center: {lat: latitude, lng: longitude}
//     });
//     fetch('/api/locations')
// .then(response => response.json())
// .then(data => {
//   console.log(data);  
//   data.forEach(location => {
//     const marker = new google.maps.Marker({
//       position: { lat: parseFloat(location.latitude), lng: parseFloat(location.longitude) },
//       map: gamesMap,
//       title: location.latitude,
//     });
//   });
// })
//   } else {
//     alert('Geocode was not successful for the following reason: ' + status);
//   }
// });

// fetch('/api/locations')
// .then(response => response.json())
// .then(data => {
//   console.log(data);  
//   data.forEach(location => {
//     const marker = new google.maps.Marker({
//       position: { lat: parseFloat(location.latitude), lng: parseFloat(location.longitude) },
//       map: gamesMap,
//       title: location.latitude,
//     });
//   });
// })
// }
}