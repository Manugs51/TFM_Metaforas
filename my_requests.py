import requests

def my_request_get(url):
    while True:
        try:
            response = requests.get(url, timeout=5)
            return response  # Return the JSON response if the request was successful
        except requests.Timeout:
            print("Timeout occurred, retrying...")

    return None  # Return None if the request was not successful after max_retries attempts
