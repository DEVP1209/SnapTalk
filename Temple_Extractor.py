import os
import shutil

def copy_and_rename_images(src_folder, dest_folder):
    # Iterate through the temple directories in the source folder
    for temple_folder in os.listdir(src_folder):
        temple_dir = os.path.join(src_folder, temple_folder)

        # Skip if it's not a folder
        if not os.path.isdir(temple_dir):
            continue

        # Start count at 1 for each temple folder
        count = 1

        # Process all images in the temple folder
        for img_file in os.listdir(temple_dir):
            img_path = os.path.join(temple_dir, img_file)

            # Only process image files (you can add more extensions if needed)
            if img_file.lower().endswith(('.jpg', '.jpeg', '.png')):
                # Create new image name: folder_name_count.jpg
                new_img_name = f"{temple_folder}_{count}.jpg"
                new_img_path = os.path.join(dest_folder, new_img_name)

                # Copy image to the destination folder with the new name
                shutil.copy(img_path, new_img_path)
                count += 1

# Define source and destination directories
source_folder = '/Users/mukeshpatel/Downloads/indian_temples'  # Folder containing temple subfolders
destination_folder = '/Users/mukeshpatel/Documents/7TH SEMESTER/SnapTalk/Dataset/images/'  # Destination folder where images will be copied

# Create destination folder if it doesn't exist
if not os.path.exists(destination_folder):
    os.makedirs(destination_folder)

# Copy and rename the images
copy_and_rename_images(source_folder, destination_folder)

print("Images copied and renamed successfully!")