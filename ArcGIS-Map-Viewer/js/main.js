require([
  "esri/Map",
  "esri/views/MapView",
  "esri/widgets/Search",
  "esri/widgets/Zoom",
  "esri/widgets/ScaleBar",
  "esri/layers/FeatureLayer"
], function(Map, MapView, Search, Zoom, ScaleBar, FeatureLayer) {
  // Basemap Initialization
  const map = new Map({ basemap: "topo-vector" });

  // Feature Layer: USA States (public ArcGIS Online layer)
  const featureLayer = new FeatureLayer({
    url: "https://services.arcgis.com/P3ePLMYs2RVChkJx/arcgis/rest/services/USA_States_Generalized/FeatureServer/0",
    outFields: ["*"],
    popupTemplate: {
      title: "{STATE_NAME}",
      content: "Population: {POP2007}"
    }
  });

  map.add(featureLayer);

  // MapView
  const view = new MapView({
    container: "mapView",
    map: map,
    center: [-98, 39], // USA center
    zoom: 4
  });

  // Widgets
  view.ui.add(new Search({ view: view }), "top-right");
  view.ui.add(new Zoom({ view: view }), "top-left");
  view.ui.add(new ScaleBar({ view: view, unit: "dual" }), { position: "bottom-left" });

  // Layer Toggle
  document.getElementById("toggleLayer").addEventListener("change", function(e) {
    featureLayer.visible = e.target.checked;
  });

  // Mouse Coordinates
  view.on("pointer-move", function(evt) {
    const point = view.toMap({ x: evt.x, y: evt.y });
    if (point) {
      document.getElementById("coords").textContent = `Lat: ${point.latitude.toFixed(4)}, Lon: ${point.longitude.toFixed(4)}`;
    }
  });

  // Responsive map resize handled by ArcGIS API
});
