import os
import shutil

def copy_and_rename_images(src_folder, dest_folder):
    # Create destination folder if it doesn't exist
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)

    # Initialize the image count to keep track of image renaming
    count = 1

    # Iterate through the test and train directories
    for main_dir in ['test', 'train']:
        main_src_dir = os.path.join(src_folder, main_dir)

        # Loop through each subfolder (Indian monument folders)
        for monument_folder in os.listdir(main_src_dir):
            monument_dir = os.path.join(main_src_dir, monument_folder)

            # Skip if it's not a folder
            if not os.path.isdir(monument_dir):
                continue

            # Process all images in the monument folder
            for img_file in os.listdir(monument_dir):
                img_path = os.path.join(monument_dir, img_file)

                # Only process image files (you can add more extensions if needed)
                if img_file.lower().endswith(('.jpg', '.jpeg', '.png')):
                    # Create new image name: folder_name_count.jpg
                    new_img_name = f"{monument_folder}_{count}.jpg"
                    new_img_path = os.path.join(dest_folder, new_img_name)

                    # Copy image to the destination folder with the new name
                    shutil.copy(img_path, new_img_path)
                    count += 1

# Define source and destination directories
source_folder = '/Users/mukeshpatel/Downloads/Indian-monuments/images'
destination_folder = '/Users/mukeshpatel/Documents/7TH SEMESTER/SnapTalk/Dataset'

# Create a single folder for all images in the copied dataset
images_folder = os.path.join(destination_folder, 'images')

# Copy and rename the images
copy_and_rename_images(source_folder, images_folder)

print("All images copied and renamed into one folder successfully!")