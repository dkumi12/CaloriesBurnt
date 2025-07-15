import base64
import os

def get_base64_encoded_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode('utf-8')

# Get base64 encoded logo
logo_path = os.path.join(os.path.dirname(__file__), "static", "metriburn_logo_new.png")
logo_base64 = get_base64_encoded_image(logo_path)

# Create a file with the base64 encoded logo
output_file = os.path.join(os.path.dirname(__file__), "logo_base64.py")
with open(output_file, 'w') as f:
    f.write(f'LOGO_BASE64 = "{logo_base64}"')

print(f"Base64 encoded logo saved to {output_file}")
