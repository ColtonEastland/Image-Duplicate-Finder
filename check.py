import os
from PIL import Image, ImageChops
from hashlib import md5
import shutil

# Define the folder to search for duplicate images
folder = input("Enter image folder path: ")

# Define the folder to move duplicate images to
duplicate_folder_name = "Duplicates"

# Create a dictionary to store the image hashes and filenames
image_data = {}

# Loop through all the files in the folder
for root, dirs, files in os.walk(folder):
    # Create the "Duplicates" folder if it doesn't already exist
    duplicate_folder = os.path.join(root, duplicate_folder_name)
    if not os.path.exists(duplicate_folder):
        os.makedirs(duplicate_folder)
    for filename in files:
        try:
            # Open the image file and calculate the MD5 hash of its contents
            image = Image.open(os.path.join(root, filename))
            hash = md5(image.tobytes()).hexdigest()

            # Check if the hash is already in the dictionary
            if hash in image_data:
                # If the image is a duplicate, move it to the "Duplicates" folder within the input directory
                shutil.move(os.path.join(root, filename), os.path.join(duplicate_folder, filename))
                # Add the duplicate image filename to the list of filenames for this hash
                image_data[hash]['filenames'].append(os.path.join(root, filename))
            else:
                # If the image is not a duplicate, add it to the dictionary with its hash and filename
                image_data[hash] = {'image': image, 'filenames': [os.path.join(root, filename)]}
        except:
            # If the file cannot be read, skip it
            pass

# Print the filenames of all duplicate images
for hash, data in image_data.items():
    if len(data['filenames']) > 1:
        print(f"Duplicate images with hash {hash}:")
        for filename in data['filenames']:
            print(filename)