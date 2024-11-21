import requests
import json
import os
from pymongo import MongoClient, errors
from bson import ObjectId
from colorama import Fore, Back, Style


class PowerfleetAPIManager:
    def __init__(self, start_date, end_date, rel_txt_path='./Powerfleet_API_CredentialsI.txt,', vehicleId=7):
        self.CREDENTIALS_FILE_PATH  = rel_txt_path
        self.START_DATE             = start_date
        self.END_DATE               = end_date
        self.VEHICLE_ID             = vehicleId
        
        self.URL = 'https://powerfleet.net/POWERFLEET5000/tr_rest/secure/vehicle/vehicle-gps-data'
        self.HEADERS = {
            'Content-Type': 'application/json'  # Authorization header will be added dynamically
        }
        self.DATA = {
            "startDate": self.START_DATE,
            "endDate": self.END_DATE,
            "vehicleId": self.VEHICLE_ID
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
            print(f"Error: The file '{self.CREDENTIALS_FILE_PATH}' was not found.")
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
            print(f"Headers: {self.HEADERS}")
            print(f"Data: {self.DATA}")

            # Make the API request
            response = requests.post(self.URL, headers=self.HEADERS, json=self.DATA)

            if response.status_code == 200:
                print(Fore.GREEN + "Success: 200")
                pretty_json = json.dumps(response.json(), indent=4)
                print(pretty_json)
                print(Style.RESET_ALL)
                return response.json()
            else:
                print(Fore.RED + f"Failed with status code {response.status_code}:")
                print(Fore.RED + response.text)
                print(Style.RESET_ALL)
                return None
        else:
            print(Fore.RED + "Error: Missing 'cid' or 'api_key' in the credentials file.")
            print(Style.RESET_ALL)
            return None

    
class DataBaseConnector:
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




