import requests
import math
import datetime



class ApiKeys:
    def __init__(self):
        self.maps_tiles_api_key = "AIzaSyA9wp-nm6AiiIRm3wMsXyUSQwmvTPr9yGU"
        # Add more API keys as needed

class BaseRequest:
    def __init__(self, api_keys):
        self.api_keys = api_keys
        self.log_file = "request_log.txt"  # Path to the log file
    
    def make_request(self, url, payload):
        api_key = self.api_keys.maps_tiles_api_key
        
        headers = {"Content-Type": "application/json"}
        
        try:
            response = requests.post(url + "?key=" + api_key, json=payload, headers=headers)
            response.raise_for_status()  # Raise exception for non-200 status codes
            return response.json()
        except requests.exceptions.RequestException as e:
            print("Error:", e)
            raise self.SessionTokenError(self.__class__.__name__, "=> Error: Failed to retrieve session token.")
    
    def write_to_log(self, url, payload, session_response):
        timestamp = datetime.datetime.now().strftime("%H:%M")
        with open(self.log_file, "a") as f:
            f.write(f"----[{timestamp}]----\n")
            f.write(f"URL: {url}\n")
            f.write(f"Payload: {payload}\n")
            f.write(f"Session Request Response: {session_response}\n")
            f.write("\n")
    
    def lat_lng_to_tile_coords(self, lat, lng, zoom):
        n = 2 ** zoom
        x_tile = int(n * ((lng + 180) / 360))
        lat_rad = math.radians(lat)
        y_tile = int(n * (1 - (math.log(math.tan(lat_rad) + 1 / math.cos(lat_rad)) / math.pi)) / 2)
        return x_tile, y_tile

class MapTilesAPI(BaseRequest):
    def __init__(self, api_keys):
        super().__init__(api_keys)
    
    def get_map_tiles(self, lat, lng, zoom):
        x_tile, y_tile = self.lat_lng_to_tile_coords(lat, lng, zoom)
        url = f"https://maps.googleapis.com/maps/api/tile"
        payload = {
            "zoom": zoom,
            "x": x_tile,
            "y": y_tile,
            "key": self.api_keys.maps_tiles_api_key
        }
        return self.make_request(url, payload)

class SessionTokenRequest(BaseRequest):
    class SessionTokenError(Exception):
        pass
    
    def __init__(self, api_keys):
        super().__init__(api_keys)
    
    def request_session_token(self):
        url = "https://tile.googleapis.com/v1/createSession"
        payload = {
            "mapType": "streetview",
            "language": "en-US",
            "region": "US"
        }
        response = self.make_request(url, payload)
        return response

# Example usage:
session_token = ""
api_keys = ApiKeys()
session_request = SessionTokenRequest(api_keys)
try:
    session_request_response = session_request.request_session_token()
    # Define payload
    payload = {
        "mapType": "streetview",
        "language": "en-US",
        "region": "US"
    }
    # Create an instance of BaseRequest to use write_to_log method
    base_request = BaseRequest(api_keys)
    base_request.write_to_log("https://tile.googleapis.com/v1/createSession", payload, session_request_response)
except SessionTokenRequest.SessionTokenError as e:
    print(f"{e.args[0]}: {e.args[1]}")
session_token = session_request_response["session"]
