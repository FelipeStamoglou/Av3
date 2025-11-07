import requests

URL = "http://localhost:8080"
NUM_REQUESTS = 10

for i in range(NUM_REQUESTS):
    try:
        response = requests.get(URL)
        # Assumindo que cada Flask retorna algo identificável, como o container
        print(f"Request {i+1}: {response.text.strip()}")
    except requests.exceptions.RequestException as e:
        print(f"Request {i+1} failed: {e}")
