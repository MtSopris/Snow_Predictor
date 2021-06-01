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

d3.json(snow_url, function(snowData){
  createFeatures(snowData.features);
//using the d3.json data, create function to bind pop, and add circle layer
  function createFeatures(snowData){
    var snowfall = L.geoJson(snowData,{
      //use onEachFeature function to bind popup/data to each created feature
      onEachFeature(feature,layer){
        layer.bindPopup("<h2> Location: "+ feature.properties.station_name +"</h2> <hr> <h2> Elevation: " 
        + feature.properties.elevation +"</h2> <hr> <h2> Powder Prediction:" + feature.properties.predicted_snow)+"</h2>";
      },
      //A Function defining how GeoJSON points spawn Leaflet layers.
    // It is internally called when data is added, passing the GeoJSON point feature and its LatLng. 
    pointToLayer(station1,latlng){
      return new L.circle(latlng,
        {
        fillOpacity: .50,
        fillColor: snowColors(snow_bins[feature['properties']['snow_prediction']]),// snowColors(snow_bins[station1['properties']['snow_prediction']]) // snowColors(6)||| station1 => {type: , geometry, properties}
        color: "#000000",
        radius: snowRadius(snow_bins[feature['properties']['snow_prediction']]),
        stroke: true,
        weight: 0.5 
        })
        }
    }).addTo(myMap);

  //setup the legend
  var legend = new L.control({position: "bottomright"});

  legend.onAdd=function(myMap){
    var div=L.DomUtil.create("div","info legend");
    //using bin values from labels in snowlevels
    var snow_bins={'5ft-28ft': 6, 
                   '2ft-5ft': 5, 
                   '12in-24in': 4, 
                   '6in-12in': 3, 
                   '3in-6in': 2, 
                   '0in-3in': 1, 
                   'melting 3in-0in': -1, 
                   'melting 6in-3in': -2, 
                   'melting 12in-6in': -3, 
                   'melting 5ft-1ft': -4,
                   'melting 28ft-5ft':-5}

    var snowlevels = [-5,-4,-3,-2,-1,1,2,3,4,5,6];
    var colors=["#99FF33","#CC00FF","#FF0066","#FF3300","#FF99FF","#66FFFF","#99FF33","#CC00FF","#FF0066","#FF3300","#000000"];
    var labels=[];

    //Add legend header and markers
    var legendInfo="<h3>Legend</h3>"+
      "<div class=\"labels\>"+
        "<div class=\"min\">"+snowlevels[0]+"</div>"+
        "<div class=\"max\">"+snowlevels[snowlevels.length-1]+"</div>"+
      "</div>";

    div.innerHTML=legendInfo;

    snowlevels.forEach(function(snowlevel,index){
      labels.push("< i style=\"background:"+colors[index]+"\"></i>");
      console.log(snowlevel);
      console.log(index);
    });

    div.innerHTML += "<ul>"+labels.join(" ")+"<ul>";
    return div;
  };
  //add legend to map
  legend.addTo(myMap);
};
   function snowColors(predicted_snow){
      if (predicted_snow=6){
        return '#000000'}
      else if (predicted_snow=5){
        return "#FF3300"}
      else if (predicted_snow=4){
        return "#FF0066"}
      else if (predicted_snow=3){
        return "#CC00FF"}
      else if (predicted_snow=2){
        return "#99FF33"}
      else if (predicted_snow=1){
        return "#66FFFF"}
      else if (predicted_snow=-1){
        return "#FF99FF"}
      else if (predicted_snow=-2){
        return "#FF3300"}
      else if (predicted_snow=-3){
        return "#FF0066"}
      else if (predicted_snow=-4){
        return "#CC00FF"}
      else {
        return "#99FF33"}

   // function snowColors(predicted_snow){
   //    if (predicted_snow='5ft-28ft'){
   //      return '#000000'}
   //    else if (predicted_snow='2ft-5ft'){
   //      return "#FF3300"}
   //    else if (predicted_snow='12in-24in'){
   //      return "#FF0066"}
   //    else if (predicted_snow='6in-12in'){
   //      return "#CC00FF"}
   //    else if (predicted_snow='3in-6in'){
   //      return "#99FF33"}
   //    else if (predicted_snow='0in-3in'){
   //      return "#66FFFF"}
   //    else if (predicted_snow='melting 3in-0in'){
   //      return "#FF99FF"}
   //    else if (predicted_snow='melting 6in-3in'){
   //      return "#FF3300"}
   //    else if (predicted_snow='melting 12in-6in'){
   //      return "#FF0066"}
   //    else if (predicted_snow='melting 5ft-1ft'){
   //      return "#CC00FF"}
   //    else {
   //      return "#99FF33"}

    };

    // function snowRadius(snow_bins[feature['properties']['snow_prediction']]) {
    //   return snow_bins[feature['properties']['snow_prediction']] *1000;
    // }
});
