import Google_APIs_Tools as google_api_tools
import requests
import json



def main():
    # Create an instance of ApiKeys
    api_keys = google_api_tools.ApiKeys()
    
    # Create an instance of SessionTokenRequest
    session_request = google_api_tools.SessionTokenRequest(api_keys)
    
    try:
        # Request a session token
        session_request_response = session_request.request_session_token()
        print(session_request_response)
    except google_api_tools.SessionTokenRequest.SessionTokenError as e:
        print(f"{e.args[0]}: {e.args[1]}")
        
        
def make_get_request(url):
    try:
        response = requests.get(url)
        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            print("Request successful!")
            data = json.loads(response.text)
            x_tile = data.get("xTile")
            y_tile = data.get("yTile")
            zoom = data.get("zoom")
            print("xTile:", x_tile)
            print("yTile:", y_tile)
            print("zoom:", zoom)
        else:
            print(f"Request failed with status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    # main()
    # indicative response: {"xTile":75,"yTile":96,"zoom":8}
    url = "http://localhost:8083/toxy?zoom=8&lng=-74.0060&lat=40.7128"  # request for localhost
    make_get_request(url)
