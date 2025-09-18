from pathlib import Path
from PIL import Image
import hashlib

def quality_control_pipeline(dataset_dir):
    issues = {
        'low_quality': [],
        'duplicates': [],
        'corrupted': [],
        'wrong_content': []
    }
    
    image_hashes = {}
    
    for image_path in Path(dataset_dir).rglob('*.jpg'):
        try:
            # Check for corruption
            with Image.open(image_path) as img:
                img.verify()
            
            # Calculate hash for duplicate detection
            img_hash = calculate_image_hash(image_path)
            if img_hash in image_hashes:
                issues['duplicates'].append((image_path, image_hashes[img_hash]))
            else:
                image_hashes[img_hash] = image_path
            
            # Quality assessment
            quality_score = assess_image_quality(image_path)
            if quality_score < 0.3:
                issues['low_quality'].append((image_path, quality_score))
                
        except Exception as e:
            issues['corrupted'].append((image_path, str(e)))
    return issues

def calculate_image_hash(image_path):
    """Calculate a hash for the image file for duplicate detection."""
    with Image.open(image_path) as img:
        img = img.convert('RGB')
        img_bytes = img.tobytes()
        return hashlib.md5(img_bytes).hexdigest()

def assess_image_quality(image_path):
    """Dummy quality assessment: returns a float between 0 and 1."""
    # TODO: Replace with real quality assessment logic
    # For now, return 1.0 for all images (high quality)
    return 1.0


def main():
    print("Kolam Dataset Quality Control")
    base_dir = Path(__file__).resolve().parent.parent 
    dataset_dir = base_dir / "processed_images"
    issues = quality_control_pipeline(dataset_dir)
    print("\nQuality Control Summary:")
    print(f"Low quality images: {len(issues['low_quality'])}")
    print(f"Duplicate images: {len(issues['duplicates'])}")
    print(f"Corrupted images: {len(issues['corrupted'])}")
    print(f"Wrong content images: {len(issues['wrong_content'])}")
    # Optionally, print details for each issue type
    for key, items in issues.items():
        if items:
            print(f"\n{key.title()} ({len(items)}):")
            for entry in items:
                print(entry)


if __name__ == "__main__":
    main()
