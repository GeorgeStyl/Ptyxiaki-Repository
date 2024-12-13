import requests
import json
import os
from pymongo import MongoClient, errors
from bson import ObjectId
from colorama import Fore, Back, Style
import sys #* For printing caught exceptions


class PowerFleetAPIsManager:
    def __init__(self, api_parameters):
        """
        Initialize the manager with specific API parameters.
        :param api_parameters: The dictionary containing API parameters.
        """
        self.PARAMETERS_REQUEST = api_parameters  # it's a dictionary
        self.CID                = self.PARAMETERS_REQUEST["cid"]
        self.API_KEY            = self.PARAMETERS_REQUEST["api_key"]

    def get_live_data(self):
        """
        Get live data from the API using the provided parameters.
        """
        print("**Live API**")
        
        URL = self.PARAMETERS_REQUEST["url"]
        HEADERS = {"Content-Type": "application/json", "Authorization": self.API_KEY}

        
        if self.PARAMETERS_REQUEST["plate"] == "": PARAMS = {"plate": ""}
        else: PARAMS = {"plate": self.PARAMETERS_REQUEST["plate"]}
        
        try:
            response = requests.get(URL, headers=HEADERS, params=PARAMS)
            # print(response)
            
            # Raise an exception for HTTP error responses (status codes 4xx and 5xx)
            response.raise_for_status()
            
            try:
                data    = response.json()
                data    = json.dumps(data, indent=4)
                print(Fore.GREEN + "Live API Request Successful!" + Style.RESET_ALL)
                # print("Response:", data)
                return data
            except ValueError:
                print(Fore.RED + "Failed to parse JSON response.")
                print("Response Text:", response.text + Style.RESET_ALL)
                return None

        except requests.exceptions.Timeout:
            print(Fore.RED + "Request timed out. Please try again later." + Style.RESET_ALL)
            return None
        except requests.exceptions.TooManyRedirects:
            print(Fore.RED + "Too many redirects. The URL might be incorrect." + Style.RESET_ALL)
            return None
        except requests.exceptions.RequestException as e:
            # Catch any other request-related errors
            print(Fore.RED + f"An error occurred with the request: {e}" + Style.RESET_ALL)
            return None
                

    
    def get_snapshot_data(self, vehicleId, startDate, endDate):
        """
        Get Snapshot data from the API using the provided parameters.
        :param vehicleID: The target vehicle ID 
        """
        print("**Snapshot API**")
        
        # Get URL and API Key from parameters
        URL     = self.PARAMETERS_REQUEST["url"]
        HEADERS = {"Content-Type": "application/json", "Authorization": self.API_KEY}
        
        # Define parameters as a dictionary
        PARAMS  = {
            "vehicleId":    vehicleId,
            "startDate":    startDate,
            "endDate":      endDate
        }
        # postdata: { startDate: "2024-01-01 00:00:00",  endDate: "2024-11-25 16:30:00", vehicleId: 7 }
        # print("Request Body:", json.dumps(PARAMS, indent=4))
        try:
            # Make the GET request with the dictionary of parameters
            response = requests.post(URL, headers=HEADERS, json=PARAMS)
            # print()
            # print(response)
            
            # Raise an exception for HTTP error responses (status codes 4xx and 5xx)
            response.raise_for_status()

            try:
                # Attempt to parse the JSON response
                data    = response.json()
                data    = json.dumps(data, indent=4)
                print(Fore.GREEN + "Snapshot API Request Successful!" + Style.RESET_ALL)
                return data
            except ValueError:
                print(Fore.RED + "Failed to parse JSON response." + Style.RESET_ALL)
                print(Fore.RED + "Response Text:", response.text + Style.RESET_ALL)
                return None

        except requests.exceptions.Timeout:
            print(Fore.RED + "Request timed out. Please try again later." + Style.RESET_ALL)
            return None
        except requests.exceptions.TooManyRedirects:
            print(Fore.RED + "Too many redirects. The URL might be incorrect." + Style.RESET_ALL)
            return None
        except requests.exceptions.RequestException as e:
            # Catch any other request-related errors
            print(Fore.RED + f"An error occurred with the request: {e}" + Style.RESET_ALL)
            return None



class MongoDBConnector:
    def __init__(self, mongoclient="mongodb://localhost:27017/", client="Ptyxiaki", mycollection="Powerfleet GPS"):
        self.client = MongoClient(mongoclient)
        self.database = self.client[client]
        self.collection = self.database[mycollection]

    def check_connection(self):
        try:
            self.client.server_info()  # Test connection
            print("Connection to MongoDB is successful!")
            return True
        except errors.ServerSelectionTimeoutError as e:
            print(f"Could not connect to MongoDB: {e}")
            return False

    def upsert_vehicle_data(self, vehicle_data_list):
        """
        Inserts or updates documents in the MongoDB collection based on `vehicleId`.

        Parameters:
            vehicle_data_list (list): List of dictionaries containing vehicle information.

        Returns:
            None
        """
        for vehicle_data in vehicle_data_list:
            self.collection.update_one(
                {"vehicleId": vehicle_data["vehicleId"]},  # Query to match `vehicleId`
                {"$set": vehicle_data},                    # Fields to update or set
                upsert=True                                # Insert if no match is found
            )
            print(f"Upserted document for vehicleId {vehicle_data['vehicleId']}.")
