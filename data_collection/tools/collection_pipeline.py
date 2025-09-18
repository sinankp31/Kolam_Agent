from pathlib import Path
import time

import argparse
import json

class KolamDatasetBuilder:
    def __init__(self, base_dir="kolam_dataset"):
        self.base_dir = Path(base_dir)
        self.setup_directories()
        self.collected_urls = set()
        self.metadata = []
    
    def collect_from_source(self, source_name, urls, category):
        print(f"Collecting from {source_name}...")
        
        for url in urls:
            time.sleep(2)  # Rate limiting
            
            try:
                images = self.scrape_page(url)
                for img_data in images:
                    if img_data['url'] not in self.collected_urls:
                        result = self.process_and_save(img_data, category)
                        if result:
                            self.metadata.append(result)
                            self.collected_urls.add(img_data['url'])
                
                print(f"✓ Processed {url}: {len(images)} images")
                
            except Exception as e:
                print(f"✗ Failed {url}: {e}")
        
        self.save_metadata()
        print(f"Completed {source_name}: {len(self.metadata)} total images")



def main():
    print("Kolam Dataset Collection Pipeline")
    source = input("Enter source name (e.g., website name): ")
    urls_file = input("Enter path to a JSON file containing a list of URLs to scrape: ")
    category = input("Enter category name for the images: ")
    base_dir = input("Enter base directory for the dataset [kolam_dataset]: ") or "kolam_dataset"

    with open(urls_file, 'r', encoding='utf-8') as f:
        urls = json.load(f)

    builder = KolamDatasetBuilder(base_dir=base_dir)
    builder.collect_from_source(source, urls, category)


if __name__ == "__main__":
    main()
