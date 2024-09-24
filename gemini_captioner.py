import os
import time
import requests
import pandas as pd

# Function to call Gemini API and get captions
def get_caption_from_gemini(image_path, api_url, api_key):
    with open(image_path, 'rb') as image_file:
        files = {'file': image_file}
        headers = {'Authorization': f'Bearer {api_key}'}
        response = requests.post(api_url, headers=headers, files=files)
        
        if response.status_code == 200:
            # Extract caption from the API response (assumed as 'caption')
            return response.json().get('caption', 'No caption found')
        else:
            print(f"Error: {response.status_code} for {image_path}")
            return 'Error in fetching caption'

def caption_images_in_folder(folder_path, api_url, api_key, csv_output_path):
    # Prepare a list to store image filenames and captions
    data = []

    # Rate limit handling: 120 requests per second
    rate_limit = 120
    request_interval = 1 / rate_limit  # Time between requests

    # Iterate over each image in the dataset folder
    for idx, image_file in enumerate(os.listdir(folder_path)):
        if image_file.lower().endswith(('.jpg', '.jpeg', '.png')):
            image_path = os.path.join(folder_path, image_file)

            # Fetch caption from Gemini API
            caption = get_caption_from_gemini(image_path, api_url, api_key)

            # Append the filename and caption to the data list
            data.append([image_file, caption])

            # Rate limiting (pause after each request)
            time.sleep(request_interval)

            # Print progress
            print(f"Processed {idx + 1}/{len(os.listdir(folder_path))}: {image_file}")

    # Create a DataFrame and save it as a CSV
    df = pd.DataFrame(data, columns=['filename', 'caption'])
    df.to_csv(csv_output_path, index=False)
    print(f"CSV file saved to {csv_output_path}")

# Configuration: Set your Gemini API URL and API Key here
api_url = 'https://api.gemini.com/caption'  # Replace with the actual Gemini API URL
api_key = 'your_gemini_api_key'  # Replace with your Gemini API key

# Define paths
dataset_folder = 'dataset'  # Folder where images are stored
output_csv = 'image_captions.csv'  # Output CSV file

# Start captioning process
caption_images_in_folder(dataset_folder, api_url, api_key, output_csv)