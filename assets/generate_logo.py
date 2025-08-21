import os
from PIL import Image, ImageDraw, ImageFont
import numpy as np

# Create a new image with a transparent background
width, height = 200, 200
image = Image.new('RGBA', (width, height), (0, 0, 0, 0))
draw = ImageDraw.Draw(image)

# Draw a circular background
center = (width // 2, height // 2)
radius = 95
background_color = (30, 30, 30, 255)  # Dark gray

# Create the circle
for y in range(height):
    for x in range(width):
        # Calculate the distance from the center
        distance = np.sqrt((x - center[0]) ** 2 + (y - center[1]) ** 2)
        if distance <= radius:
            image.putpixel((x, y), background_color)

# Draw the circle border
for y in range(height):
    for x in range(width):
        distance = np.sqrt((x - center[0]) ** 2 + (y - center[1]) ** 2)
        if radius - 1 <= distance <= radius:
            image.putpixel((x, y), (51, 51, 51, 255))  # Border color: #333

# Create a flame shape
flame_color = (229, 115, 115, 255)  # #E57373
flame_coords = [
    (100, 40),  # Top point
    (120, 60),  # Control point 1
    (140, 80),  # Control point 2
    (120, 110),  # Right point
    (110, 124),  # Bottom right
    (90, 124),   # Bottom left
    (80, 110),   # Left point
    (60, 80),    # Control point 3
    (80, 60),    # Control point 4
    (100, 40)    # Back to top
]

draw.polygon(flame_coords, fill=flame_color)

# Add text
try:
    # Try to use Arial font if available
    font = ImageFont.truetype("arial.ttf", 24)
except IOError:
    # Fallback to default font
    font = ImageFont.load_default()

text = "MetriBurn"
text_position = (width // 2, 160)
draw.text(text_position, text, fill=(255, 255, 255, 255), font=font, anchor="mm")

# Save the image as PNG
output_path = os.path.join(os.path.dirname(__file__), "metriburn_logo.png")
image.save(output_path, "PNG")

print(f"Logo saved to {output_path}")
