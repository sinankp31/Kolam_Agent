import requests
from bs4 import BeautifulSoup
import time
import os
from urllib.parse import urljoin
from pathlib import Path

class EthicalKolamScraper:

    def is_kolam_image(self, img_tag):
        # Basic filter: accept all images (customize as needed)
        # Example: filter by file extension or alt text
        src = img_tag.get('src', '').lower()
        if any(src.endswith(ext) for ext in ['.jpg', '.jpeg', '.png', '.bmp', '.gif']):
            return True
        return False

    def download_image(self, img_url, output_dir):
        # Download and save the image, return the saved file path or None
        try:
            # Handle relative URLs
            img_url_full = img_url
            if not img_url_full.startswith('http'):
                # Use the last requested URL as base
                img_url_full = urljoin(self.session.headers.get('Referer', ''), img_url)

            response = self.session.get(img_url_full, stream=True, timeout=15)
            response.raise_for_status()
            # Create output directory if it doesn't exist
            Path(output_dir).mkdir(parents=True, exist_ok=True)
            # Use the last part of the URL as filename
            filename = os.path.basename(img_url.split('?')[0])
            filepath = Path(output_dir) / filename
            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(8192):
                    f.write(chunk)
            return str(filepath)
        except Exception as e:
            print(f"Failed to download {img_url}: {e}")
            return None
    def __init__(self, delay=2):
        self.delay = delay
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Educational Research Bot (Kolam Pattern Analysis)',
            'Accept': 'text/html,application/xhtml+xml'
        })
    
    def scrape_page(self, url, output_dir):
        time.sleep(self.delay)  # Ethical delay
        
        response = self.session.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        images = soup.find_all('img', src=True)
        collected = []
        
        for img in images:
            if self.is_kolam_image(img):
                result = self.download_image(img['src'], output_dir)
                if result:
                    collected.append(result)
        
        return collected


if __name__ == "__main__":
    # Set your URL and output directory here
    url = "https://stock.adobe.com/in/search?k=muggulu"  # <-- Replace with your target URL
    output_dir = "./images"       # <-- Replace with your desired output directory
    delay = 2                     # You can change the delay if needed

    scraper = EthicalKolamScraper(delay=delay)
    collected = scraper.scrape_page(url, output_dir)
    print(f"Collected {len(collected)} images:")
    for img_path in collected:
        print(img_path)
