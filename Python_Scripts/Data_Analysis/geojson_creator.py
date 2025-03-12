import json
import os
from colorama import Fore, Style


class GeoJSONCreator:
    """Base class for creating and saving GeoJSON files."""
    
    def save_geojson(self, geojson_data, file_path):
        """Saves the GeoJSON data to a file."""
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(geojson_data, f, ensure_ascii=False, indent=4)
        print(Fore.GREEN + f"GeoJSON data saved to {file_path}" + Style.RESET_ALL)

class VehicleGeoJSONCreator(GeoJSONCreator):
    """Creates GeoJSON for vehicle tracking data."""
    
    def from_dataframe(self, df, file_path):
        """Converts a Pandas DataFrame to GeoJSON format and saves it."""
        features = []
        
        for _, row in df.iterrows():
            feature = {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [row["lng"], row["lat"]],
                },
                "properties": {
                    "vehicleId": row["vehicleId"],
                    "dateStored": row["dateStored"],
                    "velocity": row["velocity"],
                    "odometer": row["odometer"],
                    "engineVoltage": row["engineVoltage"],
                    "orientation": row["orientation"],
                    "acceleration": row["acceleration"],
                    "isProblem": row["isProblem"],
                },
            }
            features.append(feature)
        
        geojson_data = {
            "type": "FeatureCollection",
            "features": features,
        }
        
        self.save_geojson(geojson_data, file_path)

class RoadGeoJSONCreator(GeoJSONCreator):
    """Creates GeoJSON for road data (not from DataFrame)."""

    def from_dict(self, road_data, file_path):
        """Converts road data in dictionary format to GeoJSON and saves it."""
        coordinates = [[coord["lon"], coord["lat"]] for coord in road_data["coordinates"]]
        
        feature = {
            "type": "Feature",
            "geometry": {
                "type": "LineString",
                "coordinates": coordinates,
            },
            "properties": {
                "name": road_data["name"],
                "highway": road_data["highway"],
                "name_en": road_data["name_en"],
            },
        }
        
        geojson_data = {
            "type": "FeatureCollection",
            "features": [feature],
        }
        
        self.save_geojson(geojson_data, file_path)
