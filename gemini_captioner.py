import os
import time
import csv
from datetime import datetime
import google.generativeai as genai  # Use this alias for your Gemini API functions

# Configure the API key
genai.configure(api_key="AIzaSyAHGeqNvf9fYM8tHsLiQgvIWq0pM_ToZa4")  # Replace with your actual API key

# Constants
RATE_LIMIT = 120  # 120 requests per minute

# Function to generate a caption using the Gemini API
def get_image_caption(image_path, model):
    try:
        # Upload the image file using the genai alias
        uploaded_file = genai.upload_file(image_path)
        print(f"Uploaded {image_path}: {uploaded_file}")
        
        # Prompt the model for captioning
        Imageplace = os.path.basename(image_path).split('_')[0]
        prompt = f"i am training a image captioning modeL. give me suitable,single line caption without the use of complex word for this Image of {Imageplace},which includes the Place name and also describe the image environment settings" 
        result = model.generate_content([uploaded_file, "\n\n", prompt])
        
        # Extract the generated caption
        caption = result.text
        return caption
    except Exception as e:
        print(f"Error processing {image_path}: {e}")
        return 'Error'

# Function to load existing captions from CSV
def load_existing_captions(output_filename):
    existing_captions = {}
    if os.path.exists(output_filename):
        with open(output_filename, 'r', newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # Skip header
            for row in reader:
                existing_captions[row[0]] = row[1]  # Map filename to caption
    return existing_captions

# Function to process images and save captions to a CSV file after each iteration
def process_images(image_list, model, output_filename, existing_captions):
    # Open the CSV file in append mode
    with open(output_filename, 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)

        # Write header if the file is empty
        if os.stat(output_filename).st_size == 0:
            writer.writerow(['Image Filename', 'Caption'])

        # Process each image and save its caption immediately
        for i, image_path in enumerate(image_list):
            image_filename = os.path.basename(image_path)
            
            # Skip images that are already captioned
            if image_filename in existing_captions:
                print(f"Skipping already processed image: {image_filename}")
                continue
            
            # Generate caption for the image
            caption = get_image_caption(image_path, model)
            writer.writerow([image_filename, caption])
            
            # Print progress
            print(f"Processed {i + 1}/{len(image_list)}: {image_filename} - Caption: {caption}")

            # Respect the rate limit of 120 requests per minute
            if (i + 1) % RATE_LIMIT == 0:
                print(f"Reached {RATE_LIMIT} requests, waiting 60 seconds...")
                time.sleep(60)  # Pause to avoid rate limit violations

# Main logic
if __name__ == "__main__":
    # Path to the directory containing images
    dataset_path = 'Dataset/images'  # Replace with the actual path to your dataset

    # Get the list of image files (You can remove the [:10] limit if needed)
    image_list = [os.path.join(dataset_path, file) for file in os.listdir(dataset_path) if file.lower().endswith(('.jpg', '.jpeg', '.png'))]

    # Initialize the Generative Model (Gemini API)
    model = genai.GenerativeModel("gemini-1.5-flash")

    output_filename = f"Captions.csv"

    # Load existing captions to resume from last processed image
    existing_captions = load_existing_captions(output_filename)

    # Process the images and save captions
    process_images(image_list, model, output_filename, existing_captions)