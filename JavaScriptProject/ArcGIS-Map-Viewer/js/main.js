// ArcGIS API for JavaScript - Main Application Code
// This code initializes a map with a feature layer, adds widgets, and handles user interactions.
require([
  "esri/Map",
  "esri/views/MapView",
  "esri/widgets/Search",
  "esri/widgets/Zoom",
  "esri/widgets/ScaleBar",
  "esri/layers/FeatureLayer",
  "dojo/domReady!"
], function(Map, MapView, Search, Zoom, ScaleBar, FeatureLayer) {
  // Basemap Initialization
  // Create a new Map instance with a topographic basemap
  const map = new Map({ basemap: "topo-vector" });

  // Feature Layer: USA States (public ArcGIS Online layer)
  // This layer shows the states of the USA with population data
  const featureLayer = new FeatureLayer({
    url: "https://services.arcgis.com/P3ePLMYs2RVChkJx/arcgis/rest/services/USA_States_Generalized/FeatureServer/0",
    outFields: ["*"],
    popupTemplate: {
      title: "{STATE_NAME}",
      content: "Population: {POP2007}"
    }
  });

  // Add the feature layer to the map
  // This allows the layer to be displayed in the MapView
  map.add(featureLayer);

  // MapView
  // Create a new MapView instance to display the map
  const view = new MapView({
    container: "mapView",
    map: map,
    center: [-98, 39], // USA center
    zoom: 4
  });

  // Widgets
  // Add Search, Zoom, and ScaleBar widgets to the view
  view.ui.add(new Search({ view: view }), "top-right");
  // view.ui.add(new Zoom({ view: view }), "top-left");
  view.ui.add(new ScaleBar({ view: view, unit: "dual" }), { position: "bottom-left" });

  // Layer Toggle
  // Add a checkbox to toggle the visibility of the feature layer
  document.getElementById("toggleLayer").addEventListener("change", function(e) {
    featureLayer.visible = e.target.checked;
  });

  // Mouse Coordinates
  // Display coordinates of the mouse pointer in the map view
  view.on("pointer-move", function(evt) {
    const point = view.toMap({ x: evt.x, y: evt.y });
    if (point) {
      document.getElementById("coords").textContent = `Lat: ${point.latitude.toFixed(4)}, Lon: ${point.longitude.toFixed(4)}`;
    }
  });

  // Responsive map resize handled by ArcGIS API
});