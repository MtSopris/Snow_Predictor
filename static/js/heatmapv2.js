// Creating our initial map object
// We set the longitude, latitude, and the starting zoom level
// This gets inserted into the div with an id of 'map'
var myMap = L.map("map", {
  center: [39.1,-106.1],
  zoom: 7
});

// Adding tile layer to the map, create as variable incase needed
var streetMap =L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}', {
    attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
    maxZoom: 18,
    id: 'mapbox/streets-v11',
    tileSize: 512,
    zoomOffset: -1,
    accessToken: API_KEY
  });

streetMap.addTo(myMap);

//base url for json data pull ()
// var snow_url='http://127.0.0.1:5000/output' //change to actual prediction
var snow_url='../static/output/ml_predict_output.json' //hard code location for now

//start d3.json
d3.json(snow_url).then ((response=>{
  //console.log to see response
  // console.log(response)

  var heatArray = []
    response.forEach(function(one_station) {
      // console.log(one_station.lat)
      heatArray.push([one_station.lat, one_station.lon, one_station.predicted_snow])
    })
    // console.log(heatArray)

  //create empty list
//   var heatArray=[]
//   //start for loop
//   for(var i=0; i< response.length; i++) {
//     // not sure if best to use response[i] or reponse[i].station_name
//     var stationSelected = response[i].station_name;
// // added "predicted_snow"as the 3rd variable to give heat map a scale
//     if(stationSelected){
//       heatArray.push([station_name.lat,station_name.lon, station_name.predicted_snow]);
//     }
//   }

  var heat = L.heatLayer(heatArray,{
          radius: 100,
          blur: 35,
          maxIntensity: 88,
          opacity: 1,
          // dissipating: True
    }).addTo(myMap)
}))

// var heatArray = []
//     data.forEach(function(one_sale) {
//         heatArray.push([one_sale.lat, one_sale.lng, one_sale.num])
