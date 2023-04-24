from PIL import Image, ImageFilter
import os

# Set the path of the folder containing the images to be sharpened
folder_path = 'C:/path/to/unsharpened'

# Set the path of the folder where the sharpened images will be saved
output_path = 'C:/path/to/sharpened'

# Loop through each file in the folder
for file_name in os.listdir(folder_path):
    # Open the image file
    with Image.open(os.path.join(folder_path, file_name)) as image:
        # Apply a sharpening filter to the image
        sharpened_image = image.filter(ImageFilter.SHARPEN)

        # Save the sharpened image to the output folder
        sharpened_image.save(os.path.join(output_path, file_name))
