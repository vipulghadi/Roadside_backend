import requests
import json

url = "http://127.0.0.1:8000/api/v1/admin/support/general-issues/"

# Create the list of issues directly
payload = [
    {
        "title": "Delayed Response from Vendor",
        "description": "The vendor took too long to respond to the assistance request, leaving the customer stranded."
    },
    {
        "title": "Incorrect Service Provided",
        "description": "The vendor provided a service that didn't match the customer’s request, causing inconvenience."
    },
    {
        "title": "Inadequate Equipment",
        "description": "Vendor arrived without the necessary tools or equipment to complete the requested service."
    },
    {
        "title": "Miscommunication with Customer",
        "description": "Customer and vendor had communication issues, leading to misunderstandings about the service."
    },
    {
        "title": "Overcharging for Service",
        "description": "Customer reported that the vendor overcharged for the roadside assistance service."
    },
    {
        "title": "Unsatisfactory Service Quality",
        "description": "Customer was not satisfied with the quality of service provided by the vendor."
    },
    {
        "title": "Unauthorized Charge",
        "description": "Customer was charged for services they did not request or agree to."
    },
    {
        "title": "Vendor Unavailable",
        "description": "Vendor could not be reached or was unavailable when the service was requested."
    },
    {
        "title": "Late Arrival of Vendor",
        "description": "Vendor arrived significantly later than the scheduled or expected time."
    },
    {
        "title": "Unprofessional Behavior",
        "description": "Vendor displayed unprofessional or rude behavior towards the customer."
    },
    {
        "title": "Service Request Error",
        "description": "Customer accidentally selected the wrong service type in the app or website."
    },
    {
        "title": "Difficulty in Locating Customer",
        "description": "Vendor had trouble locating the customer’s vehicle due to inaccurate location information."
    },
    {
        "title": "Inability to Cancel Service",
        "description": "Customer was unable to cancel their request after making a mistake or changing their mind."
    },
    {
        "title": "Incomplete Service",
        "description": "Vendor was unable to fully resolve the issue, and additional assistance was required."
    },
    {
        "title": "Misleading Service Information",
        "description": "Information on the website or app about the service was misleading or unclear."
    },
    {
        "title": "Broken Down Equipment",
        "description": "Vendor's equipment or vehicle broke down on the way to the customer."
    },
    {
        "title": "Poor Customer Support",
        "description": "Customer had trouble reaching support to resolve an issue or get an update."
    },
    {
        "title": "Language Barrier",
        "description": "Vendor and customer faced difficulties due to a language barrier, affecting the service quality."
    },
    {
        "title": "Unclear Payment Options",
        "description": "Customer was unsure of how to pay the vendor or had issues with available payment methods."
    },
    {
        "title": "Inaccurate Billing Information",
        "description": "Customer received incorrect billing information after the service was completed."
    }
]


headers = {
    'Content-Type': 'application/json'
}

# Loop through each issue and send an individual POST request
for issue in payload:
    response = requests.post(url, headers=headers, data=json.dumps(issue))
    print(f"Status Code: {response.status_code}, Response: {response.text}")
