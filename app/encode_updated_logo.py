import base64
import os
from PIL import Image

def get_base64_encoded_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode('utf-8')

# Get base64 encoded logo from the updated file
logo_path = os.path.join(os.path.dirname(__file__), "static", "metriburn_logo_updated.png")

# Create a zoomed version of the logo
try:
    # Open the original image
    img = Image.open(logo_path)
    
    # Define a crop box to zoom in on the important part (left side with app name)
    # Format: (left, top, right, bottom)
    # More aggressive cropping to focus on the app name
    width = img.width
    height = img.height
    
    # Focus more tightly on the app name portion
    crop_box = (0, height * 0.25, width * 0.7, height * 0.75)
    
    # Crop the image
    zoomed_img = img.crop(crop_box)
    
    # Save the zoomed image
    zoomed_logo_path = os.path.join(os.path.dirname(__file__), "static", "metriburn_logo_zoomed.png")
    zoomed_img.save(zoomed_logo_path)
    
    # Use the zoomed logo
    logo_base64 = get_base64_encoded_image(zoomed_logo_path)
    print(f"Created and encoded zoomed logo: {zoomed_logo_path}")
except Exception as e:
    # Fallback to original if image processing fails
    logo_base64 = get_base64_encoded_image(logo_path)
    print(f"Error processing image, using original: {e}")

# Create a file with the base64 encoded logo
output_file = os.path.join(os.path.dirname(__file__), "logo_base64.py")
with open(output_file, 'w') as f:
    f.write(f'LOGO_BASE64 = "{logo_base64}"')

print(f"Base64 encoded logo saved to {output_file}")
