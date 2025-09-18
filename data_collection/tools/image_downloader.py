import requests
from PIL import Image
import hashlib
from pathlib import Path
import os

import json

def download_kolam_image(url, filename, output_dir):
    try:
        response = requests.get(url, timeout=30, stream=True)
        response.raise_for_status()
        
        # Verify image content
        content_type = response.headers.get('content-type', '')
        if not content_type.startswith('image/'):
            return None
        
        filepath = Path(output_dir) / filename
        with open(filepath, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
        
        # Verify image integrity
        try:
            with Image.open(filepath) as img:
                img.verify()
        except:
            os.remove(filepath)
            return None
        
        return {
            'url': url,
            'filepath': str(filepath),
            'size': filepath.stat().st_size,
            'hash': calculate_image_hash(filepath)
        }
    
    except Exception as e:
        print(f"Failed to download {url}: {e}")
        return None

def calculate_image_hash(filepath):
    """Calculate hash for duplicate detection"""
    with open(filepath, 'rb') as f:
        return hashlib.md5(f.read()).hexdigest()


if __name__ == "__main__":
    # Set your JSON file and output directory here
    json_file = "output.json"  # <-- Replace with your JSON file from dynamic_scrapper.py
    output_dir = "downloaded_images"  # <-- Replace with your desired output directory

    os.makedirs(output_dir, exist_ok=True)

    with open(json_file, "r", encoding="utf-8") as f:
        images = json.load(f)

    # Try to extract URLs from the JSON structure
    # If images is a list of dicts with 'src' or 'url' keys, adjust as needed
    results = []
    for img in images:
        url = img.get('src') or img.get('url') or img if isinstance(img, str) else None
        if not url:
            continue
        filename = os.path.basename(url.split('?')[0])
        result = download_kolam_image(url, filename, output_dir)
        if result:
            results.append(result)

    print(f"Downloaded {len(results)} images to {output_dir}.")
