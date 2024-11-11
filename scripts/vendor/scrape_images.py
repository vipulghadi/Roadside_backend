import json

def extract_image_links_from_har(file_path):
    """Extract all image links from a HAR file and save in a list."""
    vendor_images = []

    with open(file_path, "r") as f:
        har_data = json.load(f)
    
    # Loop through all entries and filter out image URLs
    for entry in har_data["log"]["entries"]:
        mime_type = entry["response"]["content"].get("mimeType", "")
        url = entry["request"]["url"]
        
        # Check if the MIME type starts with "image/"
        if mime_type.startswith("image/"):
            vendor_images.append(url)
    
    return vendor_images

def save_links_to_file(links, filename="vendor_images.py"):
    """Save the list of image links to a Python file as a list variable."""
    with open(filename, "w") as file:
        file.write("vendor_images = [\n")
        for link in links:
            file.write(f"    '{link}',\n")
        file.write("]\n")
    print(f"Links saved to {filename}")

# Replace 'yourfile.har' with the path to your HAR file
file_path = r"C:\Users\vipul ghadi\Desktop\www.gettyimages.in_Archive [24-11-07 14-19-39].har"
vendor_images = extract_image_links_from_har(file_path)

# Print the list of image URLs
print("Image URLs found in HAR file:")
for link in vendor_images:
    print(link)

# Save the list of image URLs to a Python file
save_links_to_file(vendor_images)
