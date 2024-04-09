"""
Code to test if the server is working.
"""
import requests


# Define the input dictionary
input_dict = {"question": "Why is superposition important for quantum computing?",
              "expectation": "Entanglement is crucial for quantum computing because it enables complex computations and correlations that are impossible in classical computings",
              "value": "Entanglement enables parallel processing, gate operations, error correction, quantum teleportation, and superposition, crucial for quantum computing's power and functionality.",
              "user_id":"home"}

# Define the URL of the Flask server endpoint
url = 'http://localhost:5000/process_answer'

# Send a POST request with the input dictionary as JSON payload
response = requests.post(url, json=input_dict)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    processed_dict = response.json()
    print("Processed dictionary:", processed_dict)
else:
    print("Error:", response.status_code)
