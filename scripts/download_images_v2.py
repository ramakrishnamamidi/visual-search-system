import os
import pandas as pd
import requests
import logging
from io import BytesIO
from PIL import Image
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import Pool, cpu_count, Queue, Process

# Logging configuration
logging.basicConfig(
    filename='download_errors.log',
    filemode='w',
    format='%(asctime)s - Image %(image_index)s - %(message)s',
    level=logging.ERROR
)

def download_image_bytes(idx, url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return idx, response.content  # return image as bytes
    except Exception as e:
        logging.error(str(e), extra={"image_index": idx + 1})
        return idx, None

def process_image(args):
    """
    Process and save a single image from bytes.
    """
    idx, image_bytes, output_dir, target_size = args
    filename = f"{(idx + 1):04d}.jpg"
    output_path = os.path.join(output_dir, filename)

    try:
        img = Image.open(BytesIO(image_bytes))
        if img.mode in ('RGBA', 'P'):
            img = img.convert('RGB')
        img.thumbnail(target_size, Image.Resampling.LANCZOS)
        img.save(output_path, 'JPEG', quality=85, optimize=True)
        return True
    except Exception as e:
        logging.error(str(e), extra={"image_index": idx + 1})
        return False

def download_images_hybrid(num_images=None, output_dir="images1", target_size=(800, 800), max_threads=32):
    os.makedirs(output_dir, exist_ok=True)
    df = pd.read_csv("test_urls.csv")
    if num_images:
        df = df.head(num_images)

    print(f"Downloading and processing {len(df)} images using threads + processes...")

    # Step 1: Multithreaded downloading
    image_data_list = []
    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        futures = [executor.submit(download_image_bytes, idx, row['photo_image_url'])
                   for idx, row in df.iterrows()]
        for future in tqdm(futures):
            idx, content = future.result()
            if content:
                image_data_list.append((idx, content, output_dir, target_size))

    # Step 2: Multiprocessing image processing
    with Pool(processes=cpu_count()) as pool:
        list(tqdm(pool.imap_unordered(process_image, image_data_list), total=len(image_data_list)))

if __name__ == "__main__":
    download_images_hybrid(num_images=None)
