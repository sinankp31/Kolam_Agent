import cv2
import numpy as np
from PIL import Image

import os
from pathlib import Path

class KolamImageProcessor:
    def extract_features(self, image):
        # Placeholder: implement actual feature extraction as needed
        return {}
    def __init__(self):
        self.target_size = (512, 512)
        self.min_size = (300, 300)
    
    def process_image(self, image_path):
        try:
            # Load and validate image
            img = cv2.imread(str(image_path))
            if img is None:
                return None
            
            # Check minimum size
            if img.shape[0] < self.min_size[0] or img.shape[1] < self.min_size[1]:
                return None
            
            # Basic processing
            processed = self.preprocess_kolam(img)
            features = self.extract_features(processed)
            
            return {
                'processed_image': processed,
                'features': features,
                'original_size': img.shape,
                'quality_score': self.calculate_quality_score(img)
            }
            
        except Exception as e:
            print(f"Processing failed for {image_path}: {e}")
            return None
    
    def preprocess_kolam(self, image):
        # Resize to standard dimensions
        resized = cv2.resize(image, self.target_size)
        
        # Enhance contrast
        lab = cv2.cvtColor(resized, cv2.COLOR_BGR2LAB)
        lab[:,:,0] = cv2.equalizeHist(lab[:,:,0])
        enhanced = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)
        
        return enhanced
    
    def calculate_quality_score(self, image):
        # Calculate blur detection using Laplacian variance
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
        
        # Calculate brightness and contrast
        brightness = np.mean(gray)
        contrast = np.std(gray)
        
        # Combine metrics (higher is better)
        quality_score = (laplacian_var * 0.4 + contrast * 0.4 + 
                        (255 - abs(brightness - 127)) * 0.2) / 100
        
        return min(max(quality_score, 0), 1)


def main():
    print("Kolam Image Processing Pipeline")

    base_dir = Path(__file__).resolve().parent.parent  # Go up to data_collection

    input_dir = base_dir / "raw_images"
    output_dir = base_dir / "processed_images"
    os.makedirs(output_dir, exist_ok=True)

    processor = KolamImageProcessor()
    for filename in os.listdir(input_dir):
        if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp')):
            image_path = os.path.join(input_dir, filename)
            result = processor.process_image(image_path)
            if result and result['processed_image'] is not None:
                out_path = os.path.join(output_dir, filename)
                cv2.imwrite(out_path, result['processed_image'])
                print(f"Processed and saved: {out_path} (Quality: {result['quality_score']:.2f})")
            else:
                print(f"Skipped (failed or low quality): {filename}")


if __name__ == "__main__":
    main()
