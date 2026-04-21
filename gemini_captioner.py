import os
import time
import csv
from datetime import datetime
import google.generativeai as genai  # Use this alias for your Gemini API functions
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Access the environment variab
api_key = os.getenv("API_KEY")
# Configure the API key
genai.configure(api_key=api_key)  # Replace with your actual API key

# Constants
RATE_LIMIT = 120  # 120 requests per minute

# Function to generate a caption using the Gemini API
def get_image_caption(image_path, model):
    try:
        # Upload the image file using the genai alias
        uploaded_file = genai.upload_file(image_path)
        print(f"Uploaded {image_path}: {uploaded_file}")
        
        # Prompt the model for captioning
        # Imageplace = os.path.basename(image_path).split('_')[0]
        image_name = os.path.basename(image_path).split('_')[0]
        # of {Imageplace},which includes the Place name and also describe the image environment settings
        # prompt = f"i am training a image captioning modeL. give me suitable,single line caption without the use of complex word for this Image " 
        # prompt = f"Generate single-line captions for traffic sign images, using the name of the sign instead of describing its shape or colors. For example, if an image shows a speed bump sign, the caption should be ‘A bump traffic sign on a street with vehicles’ instead of detailing the sign’s shape and colors. The captions should be clear, simple, and mention the environment around the sign, such as roads, vehicles, or pedestrians." 
        # prompt = f"Generate single-line captions for food item images using {food_item} as a hint in the caption. The captions should describe the food item, its appearance, and any surrounding elements, but avoid overly detailed or complex vocabulary. For example, if the food name is [pasta], the caption could be ‘A plate of pasta with tomato sauce and herbs.’ Make sure to mention any accompaniments, garnish, or serving style, while keeping [food name] as the focus of the caption." 
        # prompt = f"Generate single-line captions for images of Indian gods using {image_name} as a hint in the caption. The captions should describe the god’s appearance, pose, and any symbols or items associated with them. For example, if the god’s name is [Ganesha], the caption could be ‘Lord Ganesha seated with a lotus flower and a mouse by his side.’ Ensure the caption includes the god’s name and any significant attributes or elements in the image, while keeping the description simple and clear" 
        prompt = f"Generate single-line captions for images of Indian temples using {image_name} as a hint in the caption. The captions should describe the temple’s architecture, location, and any notable surroundings or features. For example, if the temple’s name is [Meenakshi Temple], the caption could be ‘The Meenakshi Temple with its towering gopurams and intricate carvings.’ Ensure the caption includes the temple’s name and highlights key visual or cultural details, while keeping the description simple and clear." 
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
    with open(output_filename, 'a', newline='\n', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)

        # Write header if the file is empty
        if os.stat(output_filename).st_size == 0:
            writer.writerow(['image_name', 'captions'])

        # Process each image and save its caption immediately
        for i, image_path in enumerate(image_list):
            image_filename = os.path.basename(image_path)
            
            # Skip images that are already captioned
            if image_filename in existing_captions:
                print(f"Skipping already processed image: {image_filename}")
                continue
            
            # Generate caption for the image
            caption = get_image_caption(image_path, model)
            caption = caption.replace('\n', ' ').replace('\r', '')
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
    dataset_path = '/Users/mukeshpatel/Downloads/temples/Images/'  # Replace with the actual path to your dataset

    # Get the list of image files (You can remove the [:10] limit if needed)
    image_list = [os.path.join(dataset_path, file) for file in os.listdir(dataset_path) if file.lower().endswith(('.jpg', '.jpeg', '.png'))]

    # Initialize the Generative Model (Gemini API)
    model = genai.GenerativeModel("gemini-1.5-flash")

    output_filename = f"/Users/mukeshpatel/Downloads/temples/Captions.csv"

    # Load existing captions to resume from last processed image
    existing_captions = load_existing_captions(output_filename)

    # Process the images and save captions
    process_images(image_list, model, output_filename, existing_captions)