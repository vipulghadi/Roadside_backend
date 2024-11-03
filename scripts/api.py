import requests
from final_images import  images
def send_post_request(url, data):
    try:
        response = requests.post(url, json=data)
        response.raise_for_status()
        return response.json()
    
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")  # HTTP error
    except requests.exceptions.ConnectionError as conn_err:
        print(f"Connection error occurred: {conn_err}")  # Connection error
    except requests.exceptions.Timeout as timeout_err:
        print(f"Timeout error occurred: {timeout_err}")  # Timeout error
    except requests.exceptions.RequestException as req_err:
        print(f"An error occurred: {req_err}")  # General error
    return None

# Example usage
url = "http://127.0.0.1:8000/api/v1/admin/food-items/food-item/"  # Replace with your API endpoint


for name,image in images.items():
    response_data = send_post_request(url, {
        "name":name,
        "image":image
    })
    if response_data:
        print("Request was successful:", response_data)
    else:
        print("failed for",name)
