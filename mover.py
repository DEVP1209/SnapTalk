import csv
import shutil
import os

def copy_images(csv_file, src_folder, dest_folder):
    # Ensure the destination folder exists
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)

    # Read the CSV file
    with open(csv_file, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            image_filename = row['Image Filename']
            src_path = os.path.join(src_folder, image_filename)
            dest_path = os.path.join(dest_folder, image_filename)

            # Check if the source image exists
            if os.path.exists(src_path):
                shutil.copy(src_path, dest_path)
                print(f"Copied {image_filename} to {dest_folder}")
            else:
                print(f"Image {image_filename} not found in {src_folder}")

# Example usage
csv_file = 'Captions.csv'
src_folder = 'Dataset/images'
dest_folder = 'Images'

copy_images(csv_file, src_folder, dest_folder)