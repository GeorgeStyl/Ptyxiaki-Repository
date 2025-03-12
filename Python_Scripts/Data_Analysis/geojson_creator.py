import json
import os
import logging
import pandas as pd
from typing import Dict, List

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

class VehicleGeoJSONCreator(GeoJSONCreator):
    """Creates GeoJSON for vehicle tracking data."""
    
    def from_dataframe(self, df: pd.DataFrame, geojson_file: str):
        """Converts a Pandas DataFrame to GeoJSON format and saves the GeoJSON file."""
        try:
            # Ensure datetime columns are converted to strings
            datetime_columns = ["dateStored", "dateStoredHuman", "dateOnlyStoredHuman"]
            for col in datetime_columns:
                if col in df.columns:
                    df[col] = df[col].astype(str)
            
            # Convert DataFrame to GeoJSON
            geojson_data = self.df_to_geojson(df)
            
            # Save GeoJSON file
            self.save_geojson(geojson_data, geojson_file)
            
            logging.info(f"GeoJSON file successfully written: {geojson_file}")
        except Exception as e:
            logging.error(f"Error processing GeoJSON file: {e}")
    
    def df_to_geojson(self, df: pd.DataFrame) -> Dict:
        """Converts a Pandas DataFrame to GeoJSON format."""
        geojson = {"type": "FeatureCollection", "features": []}
        
        for _, row in df.iterrows():
            feature = {
                "type": "Feature",
                "properties": {
                    "vehicleId": int(row["vehicleId"]) if "vehicleId" in df.columns and pd.notna(row["vehicleId"]) else None,
                    "dateStored": str(row["dateStored"]) if "dateStored" in df.columns else None,
                    "velocity": float(row["velocity"]) if "velocity" in df.columns and pd.notna(row["velocity"]) else 0.0,
                    "odometer": float(row["odometer"]) if "odometer" in df.columns and pd.notna(row["odometer"]) else 0.0,
                    "engineVoltage": float(row["engineVoltage"]) if "engineVoltage" in df.columns and pd.notna(row["engineVoltage"]) else 0.0,
                    "dateStoredHuman": str(row["dateStoredHuman"]) if "dateStoredHuman" in df.columns else None,
                    "dateOnlyStoredHuman": str(row["dateOnlyStoredHuman"]) if "dateOnlyStoredHuman" in df.columns else None,
                    "timeOnly": str(row["timeOnly"]) if "timeOnly" in df.columns else None,
                    "orientation": str(row["orientation"]) if "orientation" in df.columns else None,
                    "seconds_diff": float(row["seconds_diff"]) if "seconds_diff" in df.columns and pd.notna(row["seconds_diff"]) else None,
                    "acceleration": float(row["acceleration"]) if "acceleration" in df.columns and pd.notna(row["acceleration"]) else 0.0,
                    "isProblem": int(row["isProblem"]) if "isProblem" in df.columns and pd.notna(row["isProblem"]) else 0,
                    "lng": float(row["lng"]) if "lng" in df.columns and pd.notna(row["lng"]) else 0.0,
                    "lat": float(row["lat"]) if "lat" in df.columns and pd.notna(row["lat"]) else 0.0
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        float(row["lng"]) if "lng" in df.columns and pd.notna(row["lng"]) else 0.0,
                        float(row["lat"]) if "lat" in df.columns and pd.notna(row["lat"]) else 0.0
                    ]
                }
            }
            geojson["features"].append(feature)
        
        return geojson

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
                coords = row["coordinates"]
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

# Example usage:
# Load DataFrame
# df = pd.read_csv("../ARKGis/Road_Data.csv")
# road_creator = RoadGeoJSONCreator()
# road_creator.from_dataframe(df, "Αλεξάνδρου-Σούτσου", "../../DataSets/GeoJSON/Αλεξάνδρου-Σούτσου.geojson")
