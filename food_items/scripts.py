import requests
from bs4 import BeautifulSoup
import urllib.parse

def get_first_image_link(query):
    try:
        query = urllib.parse.quote(query)
        url = f"https://www.google.com/search?hl=en&tbm=isch&q={query}"

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"
        }

        response = requests.get(url, headers=headers)
        response.raise_for_status() 

        soup = BeautifulSoup(response.text, 'html.parser')

        images = soup.find_all('img')
        if len(images) > 1:
            return images[1].get('src')
        else:
            return None  
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# Example usage
query = "Golden Retriever"
image_link = get_first_image_link(query)
print("First image link:", image_link)
