from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
import json

class DynamicKolamScraper:

    def extract_image_data(self, img_element):
        # Extract src and alt attributes from the image element
        src = img_element.get_attribute('src')
        alt = img_element.get_attribute('alt')
        return {'src': src, 'alt': alt}
    def __init__(self, headless=True):
        options = webdriver.ChromeOptions()
        if headless:
            options.add_argument('--headless')
        options.add_argument('--user-agent=Educational Research Bot')
        
        self.driver = webdriver.Chrome(
            service=webdriver.chrome.service.Service(ChromeDriverManager().install()),
            options=options
        )
    
    def scrape_gallery(self, url, max_scrolls=20):
        try:
            self.driver.get(url)
            scroll_count = 0
            last_height = self.driver.execute_script("return document.body.scrollHeight")
            while scroll_count < max_scrolls:
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)
                new_height = self.driver.execute_script("return document.body.scrollHeight")
                if new_height == last_height:
                    break
                last_height = new_height
                scroll_count += 1
            # Collect image data
            images = self.driver.find_elements(By.TAG_NAME, 'img')
            return [self.extract_image_data(img) for img in images]
        except Exception as e:
            print(f"Error during scraping: {e}")
            return []


# ...existing code...

if __name__ == "__main__":
    url = "https://www.rangoliworld.org/flower-kolam-designs-gallery.html"  # <-- Replace with your target URL
    headless = True
    max_scrolls = 20

    scraper = DynamicKolamScraper(headless=headless)
    images = scraper.scrape_gallery(url, max_scrolls=max_scrolls)
    print(f"Collected {len(images)} images.")
    output_file = "image_links.txt"  # Changed to .txt

    # Write only the src links, one per line
    with open(output_file, "w", encoding="utf-8") as f:
        for img in images:
            if img['src']:
                f.write(img['src'] + "\n")
    print(f"Saved image links to {output_file}")
