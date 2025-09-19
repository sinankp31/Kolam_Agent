import requests
from PIL import Image
import hashlib
from pathlib import Path
import os

import json

def download_kolam_image(url, filename, output_dir):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            "Accept": "image/avif,image/webp,image/apng,image/*,*/*;q=0.8"
        }
        response = requests.get(url, timeout=30, stream=True, headers=headers)
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
    links_file = "image_links.txt"
    output_dir = "images"

    os.makedirs(output_dir, exist_ok=True)

    # Read image links from text file
    with open(links_file, "r", encoding="utf-8") as f:
        images = [line.strip() for line in f if line.strip()]

    results = []
    for idx, url in enumerate(images):
        if not url:
            print(f"Skipping empty URL at line {idx+1}")
            continue
        filename = os.path.basename(url.split('?')[0])
        if not filename:
            filename = f"image_{idx}.jpg"
        filename = f"{idx}_{filename}"
        print(f"Downloading: {url} -> {filename}")
        result = download_kolam_image(url, filename, output_dir)
        if result:
            results.append(result)

    print(f"Downloaded {len(results)} images to {output_dir}.")

