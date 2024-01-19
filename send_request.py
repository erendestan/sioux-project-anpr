import requests

# Send the license plate string to API
API_URL = "http://localhost:8080/parking"
license_plate = "75-DN-GP"
parking_taken = False

request = {"licensePlate": license_plate, "parkingTaken": parking_taken}

print("Sending request to API: ", request)
response = requests.post(API_URL, json=request)

print("Response from API: ", response.text)