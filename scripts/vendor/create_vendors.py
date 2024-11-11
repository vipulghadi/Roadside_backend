import requests
import json
import random
from faker import Faker


faker = Faker()

# URL and headers for the API
url = "http://127.0.0.1:8000/api/v1/client/vendor/vendor-registration/"
headers = {
    'Content-Type': 'application/json'
}

def generate_10_digit_phone():
    """Generate a random 10-digit phone number."""
    return str(random.randint(6000000000, 9999999999))  # Start with 6-9 to ensure valid mobile numbers

def generate_random_vendor_data():
    """Generate a random vendor registration payload."""
    latitude = random.uniform(8.0, 37.0)  # Rough range for latitudes in India
    longitude = random.uniform(68.0, 97.0)  # Rough range for longitudes in India

    return {
        "first_name": faker.first_name(),
        "last_name": faker.last_name(),
        "vendor_name": faker.company(),
        "address": faker.address(),
        "city": faker.city(),
        "state": faker.state(),
        "zipcode": faker.zipcode(),
        "contact_number": generate_10_digit_phone(),
        "alternate_contact_number": generate_10_digit_phone(),
        "open_at": f"{random.randint(0, 23):02}:{random.randint(0, 59):02}",  # Random opening hour in HH:MM format
        "close_at": f"{random.randint(0, 23):02}:{random.randint(0, 59):02}",  # Random closing hour in HH:MM format
        "description": faker.text(max_nb_chars=100),
        "opening_days": random.sample(["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"], random.randint(1, 7)),
        "establishment_year": random.randint(1980, 2022),  # Random year between 1980 and 2022
        "food_type": random.choice(["veg", "nonveg", "all"]),
        "location_type": random.choice(["permanent", "movable"]),
        "sitting_available": random.choice(["indoor", "outdoor", "both","not available"]),
        "size": random.choice(["small", "medium", "large"]),
        "latitude": latitude,
        "longitude": longitude
    }

def create_vendors(num_vendors):
    
    for _ in range(num_vendors):
        vendor_data = generate_random_vendor_data()
        payload = json.dumps(vendor_data)
        
        response = requests.post(url, headers=headers, data=payload)
        
        print(f"Status Code: {response.status_code}, Response: {response.text}")

# Example usage to create 10 random vendors
create_vendors(50)
