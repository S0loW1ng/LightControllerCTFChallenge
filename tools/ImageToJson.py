import json
import os
from PIL import Image

# Create the output folder if it doesn't exist
output_folder = "output"
os.makedirs(output_folder, exist_ok=True)

# Get the current directory where the script is located
current_directory = os.path.dirname(os.path.abspath(__file__))

# Get all image files in the directory (jpg and png)
image_files = [file for file in os.listdir(current_directory) if file.lower().endswith((".jpg", ".png"))]

# Process each image file
for image_file in image_files:
    try:
        input_image_path = os.path.join(current_directory, image_file)

        # Load the image
        image = Image.open(input_image_path)

        # Resize the image to 16x16
        pixel_art = image.resize((16, 16), Image.Resampling.NEAREST)

        # Convert to RGB mode (if not already)
        pixel_art = pixel_art.convert("RGB")

        # Prepare the JSON structure 
        # You can chanhe it to 16 x 32
        image_data = {"rows": 16, "cols": 16, "pixels": []}

        # Get pixel data
        pixels = pixel_art.load()

        # Collect RGB data by rows
        for y in range(16):  # Rows
            row = []
            for x in range(16):  # Columns
                r, g, b = pixels[x, y]  # Get RGB values
                row.append({"r": r, "g": g, "b": b})  # Add RGB values as a dictionary
            image_data["pixels"].append(row)

        # Save JSON file in the output folder
        output_json_path = os.path.join(output_folder, f"{os.path.splitext(image_file)[0]}.json")
        with open(output_json_path, "w") as json_file:
            json.dump(image_data, json_file, indent=4)

        print(f"JSON saved for {image_file} to {output_json_path}")
    except Exception as e:
        print(f"Error processing {image_file}: {e}")
