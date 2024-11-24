import requests
import json
import os
from pymongo import MongoClient, errors
from bson import ObjectId
from colorama import Fore, Back, Style
import sys #* For printing caught exceptions


class LivePowerfleetAPIManager:
    def __init__(self, plate="", rel_txt_path='./Powerfleet_API_Credentials.txt'):
        self.CREDENTIALS_FILE_PATH  = rel_txt_path  #* Credentials for API usage
        self.PLATE                  = plate         #* plate if set to "" fetch every vehicle
        self.REF_RATE               = 3.0           #* Refresh rate for fetching data from API
        
        #* Contsruct API request
        self.URL = 'https://powerfleet.net/POWERFLEET5000/tr_rest/secure/vehicle/gps-live-data?plate=' + self.PLATE
        self.HEADERS = {
            'Content-Type': 'application/json'  # Authorization header will be added dynamically
        }
        self.DATA = {
            "plate": self.PLATE
        }

    def get_values_from_file(self, *keys):
        """Reads the credentials file and fetches values for the given keys."""
        data = {}
        try:
            print(f"{os.getcwd()=}")
            print(f"{os.listdir()}")
            with open(self.CREDENTIALS_FILE_PATH, 'r') as file:
                for line in file:
                    line = line.strip()
                    if ':' in line:
                        key, value = line.split(':', 1)
                        data[key.strip()] = value.strip()
        except FileNotFoundError:
            print(f"Error: The file '{self.CREDENTIALS_FILE_PATH}' was not found.", file=sys.stderr)
            return None

        result = {key: data.get(key) for key in keys}
        return result

    def retrieve_response(self):
        """Fetches data from the API."""
        values = self.get_values_from_file('cid', 'api_key')
        
        if values and values.get('cid') and values.get('api_key'):
            # Update headers and data
            self.HEADERS['Authorization'] = values['api_key']
            self.DATA['cid'] = values['cid']

            # Debugging: Print the headers and data
            print(Fore.YELLOW + f"Headers: {self.HEADERS}")
            print(Fore.YELLOW + f"Data: {self.DATA}")
            print(Style.RESET_ALL)

            # Make the API request
            response = requests.get(self.URL, headers=self.HEADERS, json=self.DATA)

            if response.status_code == 200:
                print(Fore.GREEN + "Success: 200")
                pretty_json = json.dumps(response.json(), indent=4)
                print(pretty_json)
                print(Style.RESET_ALL)
                return response.json()
            else:
                print(f"Failed with status code {response.status_code}:", file=sys.stderr)
                print(response.text, file=sys.stderr)
                return None
        else:
            print("Error: Missing 'cid' or 'api_key' in the credentials file.", file=sys.stderr)
            return None


class SnapshotPowerfleetAPIManager(LivePowerfleetAPIManager):
    def __init__(self, starting_date, ending_date, vehicleId, rel_txt_path='./Powerfleet_API_Credentials.txt'):
        # Call the parent constructor to initialize base attributes
        super().__init__(rel_txt_path=rel_txt_path)

        #* Store required parameters
        self.STARTING_DATE  = starting_date
        self.ENDING_DATE    = ending_date
        self.VEHICLEID      = vehicleId

        # Update URL and DATA based on the parameters
        self.URL = 'https://powerfleet.net/POWERFLEET5000/tr_rest/secure/vehicle/vehicle-gps-data'
        self.DATA.update({
            "startDate": self.STARTING_DATE,
            "endDate": self.ENDING_DATE,
            "vehicleId": self.VEHICLEID
        })

    def retrieve_extended_response(self):
        """Fetch extended data from the API."""
        print(Fore.BLUE + "Using the Snapshot API manager..." + Style.RESET_ALL)

        # Reuse the parent `retrieve_response` method
        return self.retrieve_response()

# Example usage
if __name__ == "__main__":
    # Parameters for snapshot data
    starting_date = "2024-01-01 00:00:00"
    ending_date = "2024-11-23 23:59:59"
    vehicle_id = "7"

    # Create an instance of SnapshotPowerfleetAPIManager
    snapshot_manager = SnapshotPowerfleetAPIManager(starting_date, ending_date, vehicle_id)

    # Print the constructed URL and DATA for debugging
    print("Constructed URL:", snapshot_manager.URL)
    print("Constructed DATA:", snapshot_manager.DATA)

    # Call the retrieve_extended_response method to fetch data
    snapshot_response = LivePowerfleetAPIManager()

    # Output the result
    if snapshot_response:
        print("Snapshot data retrieved successfully!")
        print(json.dumps(snapshot_response, indent=4))
    else:
        print("Failed to retrieve snapshot data.")

    
    
# class DataBaseConnector:
    def __init__(self, created_query):
        self.DB_NAME = "Ptyxiaki"
        self.COLLECTION_NAME = "Powerfleet GPS"
        self.QUERY_TO_DB = created_query.retrieve_response()
        self.collection = None

    def get_DB_info(self):
        return self.DB_NAME, self.COLLECTION_NAME 

    def connect_to_db(self):
        try:
            client = MongoClient("localhost:27017", serverSelectionTimeoutMS=5000)
            db = client[self.DB_NAME]
            self.collection = db[self.COLLECTION_NAME]
            
            client.server_info()
            return self.collection
        
        except errors.ServerSelectionTimeoutError as e:
            print(f"Error: Could not connect to the MongoDB server. Details: {e}")
        except errors.PyMongoError as e:
            print(f"Error: An error occurred while connecting to the database. Details: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")
        return None 
        
    def insert_document(self):
        if not self.collection:
            print("Error: Database not connected. Please connect to the database first.")
            return
        
        try:
            result = self.collection.insert_one(self.QUERY_TO_DB)
            print(f"Results after inserting the response: {result.inserted_id}")
        except errors.PyMongoError as e:
            print(f"Error: Failed to insert document. Details: {e}")
        except Exception as e:
            print(f"Unexpected error while inserting document: {e}")
            




print(os.getcwd())


