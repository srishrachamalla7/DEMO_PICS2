import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urlparse, urljoin

# URL of the Google Images search results page
google_search_url = "https://www.google.co.in/search?sca_esv=568452477&q=rdr2+images&tbm=isch&source=lnms&sa=X&ved=2ahUKEwj5oevq-MeBAxVJbWwGHf0TCMEQ0pQJegQICxAB&biw=720&bih=782&dpr=1.25"

# Send an HTTP GET request to Google Images
response = requests.get(google_search_url)

# Parse the HTML content of the page
soup = BeautifulSoup(response.text, "html.parser")

# Find and download the first 7 image URLs
image_urls = []

for img in soup.find_all("img"):
    src = img.get("src")
    if src and src.startswith("http"):
        image_urls.append(src)
    else:
        data_src = img.get("data-src")
        if data_src and data_src.startswith("http"):
            image_urls.append(data_src)

# Take only the first 7 image URLs
image_urls = image_urls[:7]

# Download the images and save them to a local directory
output_dir = "data/images"
os.makedirs(output_dir, exist_ok=True)

for i, url in enumerate(image_urls):
    # Ensure that the URL is complete
    if not url.startswith("http"):
        url = urljoin(google_search_url, url)

    response = requests.get(url)
    with open(os.path.join(output_dir, f"image_{i}.jpg"), "wb") as f:
        f.write(response.content)
