// Choropleth map
// var mapboxAccessToken = API_KEY;
// var myMap = L.map("map", {
//   center: [39.001, -105.520],
//   zoom: 7
// });

// // Adding tile layer
// L.tileLayer("https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}", {
//   attribution: "© <a href='https://www.mapbox.com/about/maps/'>Mapbox</a> © <a href='http://www.openstreetmap.org/copyright'>OpenStreetMap</a> <strong><a href='https://www.mapbox.com/map-feedback/' target='_blank'>Improve this map</a></strong>",
//   tileSize: 512,
//   maxZoom: 18,
//   zoomOffset: -1,
//   id: "mapbox/streets-v11",
//   accessToken: API_KEY
// }).addTo(myMap);

// //read in data with url
// snow_url='http://127.0.0.1:5000/output' //change to actual prediction
// snow_url="../output/ml_predict_output.json"

// Load in geojson data
// d3.json(snow_url).then((response=>{
// 	var heatArray=[]
// 	Object.entries(response).forEach((station_name)=>{
// 		console.log(station_name)
// 		var lat = station_name[0]['lat'];
// 		var lon = station_name[0]['lon'];
// 		var predicted_snow=station_name[0]['predicted_snow']

// 	})
// 	console.log(heatArray)
// 	L.heatlayer(heatArray,{
// 		radius: 100,
// 		blur: 35,
// 		maxIntensity: 88,
// 		opacity: 1,
// 		dissipating: True
// 	}).addTo(myMap)
// }));
