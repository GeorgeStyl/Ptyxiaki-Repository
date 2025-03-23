import json
import os
import logging
import pandas as pd
from typing import Dict

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class GeoJSONCreator:
    """Base class for creating and saving GeoJSON files."""

    def save_geojson(self, geojson_data: Dict, file_path: str):
        """Saves the GeoJSON data to a file."""
        try:
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(geojson_data, f, ensure_ascii=False, indent=2)
            logging.info(f"GeoJSON data saved to {file_path}")
        except Exception as e:
            logging.error(f"Error saving GeoJSON: {e}")

class RoadGeoJSONCreator(GeoJSONCreator):
    """Creates GeoJSON for road data."""
    
    def from_dataframe(self, df: pd.DataFrame, road_name: str, file_path: str):
        """Extracts road data from DataFrame, converts to GeoJSON, and saves it."""
        road_data = self.get_road_data(df, road_name)
        if road_data:
            geojson_data = self.road_to_geojson(road_data)
            self.save_geojson(geojson_data, file_path)
        else:
            logging.warning(f"No data found for road: {road_name}")
    
    def get_road_data(self, df: pd.DataFrame, road_name: str) -> Dict:
        """Retrieves road data from DataFrame in dictionary format."""
        filtered_data = df[df['name'] == road_name]
        if not filtered_data.empty:
            for _, row in filtered_data.iterrows():
                coords = json.loads(row["coordinates"])
                if isinstance(coords, list):
                    return {
                        "name": row["name"],
                        "highway": row.get("highway", "Unknown"),
                        "name_en": row.get("name_en", row["name"]),
                        "coordinates": [{"lat": coord['lat'], "lon": coord['lon']} for coord in coords]
                    }
                else:
                    logging.error(f"Invalid coordinate format for road: {road_name}")
        return None
    
    def road_to_geojson(self, road_data: Dict) -> Dict:
        """Converts road data dictionary to GeoJSON format."""
        return {
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Feature",
                    "properties": {
                        "name": road_data["name"],
                        "highway": road_data["highway"],
                        "name_en": road_data["name_en"]
                    },
                    "geometry": {
                        "type": "LineString",
                        "coordinates": [[coord["lon"], coord["lat"]] for coord in road_data["coordinates"]]
                    }
                }
            ]
        }

class HouseGeoJSONCreator(GeoJSONCreator):
    """Creates GeoJSON for house/building data."""
    
    def from_dataframe(self, df: pd.DataFrame, geojson_file: str):
        """Converts a Pandas DataFrame to GeoJSON format and saves the GeoJSON file."""
        try:
            geojson_data = self.df_to_geojson(df)
            self.save_geojson(geojson_data, geojson_file)
            logging.info(f"GeoJSON file successfully written: {geojson_file}")
        except Exception as e:
            logging.error(f"Error processing GeoJSON file: {e}")
    
    def df_to_geojson(self, df: pd.DataFrame) -> Dict:
        """Converts house/building DataFrame to GeoJSON format."""
        geojson = {"type": "FeatureCollection", "features": []}
        
        for _, row in df.iterrows():
            feature = {
                "type": "Feature",
                "properties": {
                    "id": int(row["id"]),
                    "name": row["name"],
                    "building_type": row["building_type"]
                },
                "geometry": {
                    "type": "Polygon",  # Buildings are usually polygons
                    "coordinates": json.loads(row["coordinates"])  # Coordinates from the DataFrame
                }
            }
            geojson["features"].append(feature)
        
        return geojson

# Example usage:
# Load DataFrame (osm_roads, osm_houses)
# osm_roads = pd.read_csv("path_to_OSM_roads.csv")
# osm_houses = pd.read_csv("path_to_OSM_houses.csv")

# Initialize the GeoJSON creator for roads and houses
road_geojson_creator = RoadGeoJSONCreator()
house_geojson_creator = HouseGeoJSONCreator()

# Function to create and save GeoJSON for roads
def create_road_geojson(df: pd.DataFrame, output_path: str):
    for road_name in df['name'].unique():
        file_path = f"{output_path}/{road_name}.geojson"
        road_geojson_creator.from_dataframe(df, road_name, file_path)
        print(f"GeoJSON for road {road_name} saved at {file_path}")

# Convert osm_roads DataFrame to GeoJSON files for each road
create_road_geojson(osm_roads, "path_to_save_roads")  # Replace with your output path

# Function to create and save GeoJSON for houses
def create_house_geojson(df: pd.DataFrame, output_path: str):
    file_path = f"{output_path}/osm_houses.geojson"
    house_geojson_creator.from_dataframe(df, file_path)
    print(f"GeoJSON for houses saved at {file_path}")

# Conver
