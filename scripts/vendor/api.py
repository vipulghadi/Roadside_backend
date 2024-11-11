# import requests
# import random
# from final_images import vendor_images  # Assuming `vendor_images` is a list of image URLs in `final_images.py`

# # Define the base URL for the POST request
# base_url = "http://127.0.0.1:8000/api/v1/client/vendor/add-vendor-images/"

# # Function to add images to a vendor using a POST request
# def add_images_to_vendor(vendor_id, images):
#     # Randomly select 7 images from the images list
#     selected_images = random.sample(images, 7)
    
#     # Construct the payload
#     payload = {
#         "links": selected_images,
#         "vendor_id": vendor_id
#     }

#     # Send POST request with the payload as JSON data
#     response = requests.post(base_url, json=payload)

#     # Check the response status
#     if response.status_code == 200:
#         print(f"Successfully added images to vendor {vendor_id}")
#     else:
#         print(f"Failed to add images to vendor {vendor_id}. Status Code: {response.status_code}, Response: {response.text}")

# # Loop through vendor IDs from 56 to 140
# for vendor_id in range(55, 56):
#     add_images_to_vendor(vendor_id, vendor_images)

#--------------------------------------------------------------------------------------------------------------------------
#adding reviews api

import requests
import random

# API URL for posting the review
API_URL = "http://127.0.0.1:8000/api/v1/client/vendor/vendor-reviews/"  # Change this URL according to your endpoint
# Example if you have an authentication token (Add headers if needed)
HEADERS = {
    "Content-Type": "application/json",
# Remove if no auth token is needed
}

# Dummy review comments
comments = [
    "Great taste, highly recommend!",
    "Service was slow but the food was good.",
    "Average experience, nothing special.",
    "Excellent quality and fast delivery!",
    "Not satisfied with the food, too spicy.",
    "Delicious and well-presented dishes!",
    "Portions were small for the price.",
    "Amazing experience, will order again.",
    "The best vendor in town, hands down!",
    "Food arrived late and was cold."
]

# Function to generate random reviews
def generate_random_review(vendor_id):
    return {
        "vendor": vendor_id,
        "user": None,  # Rating between 1 to 5
        "comment": random.choice(comments)
    }

# Generate 4 random reviews for each vendor ID from 55 to 141
for vendor_id in range(55, 142):
    for _ in range(4):
        # Randomly pick a user ID for the review (Assuming user IDs range from 1 to 20)
        user_id = random.randint(1, 20)
        # Generate random review data
        review_data = generate_random_review(vendor_id)
        # Send POST request
        response = requests.post(API_URL, json=review_data, headers=HEADERS)
        
        # Print response for each request
        if response.status_code == 201:
            print(f"Successfully created review for vendor {vendor_id}: {response.json()}")
        else:
            print(f"Failed to create review for vendor {vendor_id}: {response.status_code}, {response.text}")
