import os
import json
import pandas as pd
from arcgis.gis import GIS
from arcgis.features import FeatureLayer
from arcgis.geometry import Geometry

# 1️⃣ Authentication and Portal Access
def authenticate(config_path='config/credentials.json'):
    with open(config_path) as f:
        creds = json.load(f)
    gis = GIS(creds['portal_url'], creds['username'], creds['password'])
    print(f"Authenticated as: {gis.users.me.username}")
    return gis

# 2️⃣ Search and List Content
# This function searches for feature layers in the portal based on a search term.
def search_feature_layers(gis, search_term="*", max_items=20):
    items = gis.content.search(query=f"{search_term} AND type:Feature Layer", item_type="Feature Layer", max_items=max_items)
    data = []
    # Collect metadata for each item
    # This will create a DataFrame and save it as a CSV file.
    for item in items:
        data.append({
            "title": item.title,
            "owner": item.owner,
            "created": item.created,
            "type": item.type,
            "id": item.id
        })
    df = pd.DataFrame(data)
    os.makedirs("results", exist_ok=True)
    df.to_csv("results/portal_content_report.csv", index=False)
    print("Saved portal content metadata to results/portal_content_report.csv")
    return items

# 3️⃣ Download Feature Layer Data
def download_layer(item, out_path="data/layer.geojson"):
    flayer = item.layers[0]
    sdf = flayer.query().sdf
    os.makedirs("data", exist_ok=True)
    sdf.to_file(out_path, driver="GeoJSON")
    print(f"Downloaded layer data to {out_path}")
    return sdf

# 4️⃣ Buffer and Spatial Analysis
def buffer_and_spatial_join(schools_sdf, crime_sdf, buffer_dist=1000):
    schools_buffer = schools_sdf.copy()
    schools_buffer['geometry'] = schools_buffer.geometry.buffer(buffer_dist)
    joined = crime_sdf.sjoin(schools_buffer, predicate='within')
    joined_count = joined.groupby('school_name').size()
    results_path = "results/analysis_results.geojson"
    joined.to_file(results_path, driver="GeoJSON")
    print(f"Spatial join results saved to {results_path}")
    return joined, joined_count

# 5️⃣ Update & Share Processed Layers
def publish_and_share(gis, results_path, title="Buffer Analysis Results", share_with="everyone"):
    item_properties = {
        'title': title,
        'type': 'GeoJson',
        'tags': 'analysis, automation',
        'description': 'Results of buffer and spatial join analysis.'
    }
    result_item = gis.content.add(item_properties, data=results_path)
    if share_with == "everyone":
        result_item.share(everyone=True)
    print(f"Published and shared: {result_item.title} ({result_item.id})")
    return result_item

if __name__ == "__main__":
    # Example workflow
    gis = authenticate()
    items = search_feature_layers(gis, search_term="parks")
    if items:
        parks_item = items[0]
        parks_sdf = download_layer(parks_item, out_path="data/parks.geojson")
        # For demo, buffer parks and join with another layer if available
        # schools_item = ... # Load another item for spatial join
        # crime_item = ...   # Load another item for spatial join
        # schools_sdf = download_layer(schools_item, out_path="data/schools.geojson")
        # crime_sdf = download_layer(crime_item, out_path="data/crime.geojson")
        # joined, joined_count = buffer_and_spatial_join(schools_sdf, crime_sdf)
        # published_item = publish_and_share(gis, "results/analysis_results.geojson")
    else:
        print("No parks feature layers found.")