from PIL import Image
import requests
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def load_image(image_path_or_url):
    if image_path_or_url.startswith("http://") or image_path_or_url.startswith("https://"):
        return Image.open(requests.get(image_path_or_url, stream=True).raw).convert("RGB")
    else:
        image_path_or_url = 'data/' + image_path_or_url
        return Image.open(image_path_or_url).convert("RGB")