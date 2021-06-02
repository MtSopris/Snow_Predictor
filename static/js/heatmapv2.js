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
console.log(snow_url)

var snow_bins={'5ft-28ft': 11, 
               '2ft-5ft': 10, 
               '12in-24in': 9, 
               '6in-12in': 8, 
               '3in-6in': 7, 
               '0in-3in': 6, 
               'melting 3in-0in': 5, 
               'melting 6in-3in': 4, 
               'melting 12in-6in': 3, 
               'melting 5ft-1ft': 2,
               'melting 28ft-5ft':1}


function styleInfo(feature){
  return { 
    fillOpacity: .50,
    fillColor: snowColors(snow_bins[feature['properties']['predicted_snow']]),// snowColors(snow_bins[station1['properties']['snow_prediction']]) // snowColors(6)||| station1 => {type: , geometry, properties}
    color: "#66FFFF",
    radius: snowRadius(snow_bins[feature['properties']['predicted_snow']]),
    stroke: true,
    weight: 0.5 
  }
}

function snowRadius(predicted_snow) {
  return Math.abs(predicted_snow) *5;
};


function snowColors(predicted_snow){
  if (predicted_snow=11){
    return '#0000ff'}
  else if (predicted_snow=10){
    return "#4D004D"}
  else if (predicted_snow=9){
    return "#8C1AFF"}
  else if (predicted_snow=8){
    return "#000080"}
  else if (predicted_snow=7){
    return "#006666"}
  else if (predicted_snow=6){
    return "#008000"}
  else if (predicted_snow=5){
    return "#608000"}
  else if (predicted_snow=4){
    return "#FFFF00"}
  else if (predicted_snow=3){
    return "#E65C00"}
  else if (predicted_snow=2){
    return "#990000"}
  else {
    return "#330000";
  };
}

d3.json(snow_url).then(data=>{
  console.log(data)
  L.geoJSON(data['features'], {
    pointToLayer: function(feature, latlng){
      return L.circleMarker(latlng);
      },
    style: styleInfo, //styleInfo(feature) 
    onEachFeature: function(feature, layer) {
      layer.bindPopup("<h2> Location: "
        + feature.properties.station_name 
        +"</h2> <hr> <h2> Elevation: " 
        + feature.properties.elevation 
        +"</h2> <hr> <h2> Powder Prediction:" 
        + feature.properties.predicted_snow
        +"</h2>"
      )
    }
  }).addTo(myMap)

  //setup the legend
  var legend= new L.control({position: "bottomright"});

  // legend.onAdd= function(myMap){
  //   //create div var using domUtil
  //   var div= L.DomUtil.create("div","info legend");
  //     div.innerHTML +="<h3>Legend</h3>";
  //     div.innerHTML +='<i style="background:#330000"></i><span>melting 28ft-5ft</span><br>';
  //     div.innerHTML +='<i style="background:#990000"></i><span>melting 5ft-1ft</span><br>';
  //     div.innerHTML +='<i style="background:#E65C00"></i><span>melting melting 12in-6in</span><br>';
  //     div.innerHTML +='<i style="background:#FFFF00"></i><span>melting 6in-3in</span><br>';
  //     div.innerHTML +='<i style="background:#608000"></i><span>melting 3in-0in</span><br>';
  //     div.innerHTML +='<i style="background:#008000"></i><span>0in-3in</span><br>';
  //     div.innerHTML +='<i style="background:#006666"></i><span>3in-6in</span><br>';
  //     div.innerHTML +='<i style="background:#008000"></i><span>6in-12in</span><br>';
  //     div.innerHTML +='<i style="background:#8C1AFF"></i><span>12in-24in</span><br>';
  //     div.innerHTML +='<i style="background:#4D004D"></i><span>2ft-5ft</span><br>';
  //     div.innerHTML +='<i style="background:#0000ff"></i><span>5ft-28ft</span><br>';

    
  //   var colors=["#330000","#990000","#E65C00","#FFFF00","#608000","#008000","#006666","#008000","#8C1AFF","#4D004D","#0000ff"]
  //   var labels =[];

  //   //Add legend header and markers
  //   var legendInfo="<h3>Legend</h3>"+
  //     "<div class=\"labels\>"+
  //       "<div class=\"min\">"+snow_bins[0]+"</div>"+
  //       "<div class=\"max\">"+snow_bins[snow_bins.length-1]+"</div>"+
  //     "</div>";   
      
  //   div.innerHTML=legendInfo; 

  //   snow_bins.forEach(function(snow_bin,index){
  //     labels.push("< i style=\"background:"+colors[index]+"\"></i>");
  //     // console.log(snowlevel);
  //     // console.log(index);
  //   });
  //   div.innerHTML += "<ul>"+labels.join(" ")+"<ul>";
  //   return div;
  // };
  // legend.addTo(myMap);
})

// d3.json(snow_url, function(snowData){
//   createFeatures(snowData.features);
//   console.log(snowData)
// //using the d3.json data, create function to bind pop, and add circle layer
// });

// function snowColors(predicted_snow){
//   // predicted_snow=snow_bins[feature['properties']['predicted_snow']];
//   if (predicted_snow='5ft-28ft'){
//     return '#0000ff'}
//   else if 
//     (predicted_snow='2ft-5ft'){
//     return "#4D004D"}
//   else if 
//     (predicted_snow='12in-24in'){
//     return "#8C1AFF"}
//   else if 
//     (predicted_snow='6in-12in'){
//     return "#000080"}
//   else if 
//     (predicted_snow='3in-6in'){
//     return "#006666"}
//   else if 
//     (predicted_snow='0in-3in'){
//     return "#008000"}
//   else if 
//     (predicted_snow='melting 3in-0in'){
//     return "#608000"}
//   else if 
//     (predicted_snow='melting 6in-3in'){
//     return "#FFFF00"}
//   else if 
//     (predicted_snow='melting 12in-6in'){
//     return "#E65C00"}
//   else if 
//     (predicted_snow='melting 5ft-1ft'){
//     return "#990000"}
//   else {
//     return "#330000";
//   };

// function snowColors(predicted_snow){
//   if (predicted_snow=6){
//     return '#0000ff'}
//   else if (predicted_snow=5){
//     return "#4D004D"}
//   else if (predicted_snow=4){
//     return "#8C1AFF"}
//   else if (predicted_snow=3){
//     return "#000080"}
//   else if (predicted_snow=2){
//     return "#006666"}
//   else if (predicted_snow=1){
//     return "#008000"}
//   else if (predicted_snow=-1){
//     return "#608000"}
//   else if (predicted_snow=-2){
//     return "#FFFF00"}
//   else if (predicted_snow=-3){
//     return "#E65C00"}
//   else if (predicted_snow=-4){
//     return "#990000"}
//   else {
//     return "#330000";
//   };
// }

// var snow_bins={'5ft-28ft': 6, 
//                '2ft-5ft': 5, 
//                '12in-24in': 4, 
//                '6in-12in': 3, 
//                '3in-6in': 2, 
//                '0in-3in': 1, 
//                'melting 3in-0in': -1, 
//                'melting 6in-3in': -2, 
//                'melting 12in-6in': -3, 
//                'melting 5ft-1ft': -4,
//                'melting 28ft-5ft':-5}