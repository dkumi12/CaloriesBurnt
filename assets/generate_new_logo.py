import os
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import math

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

# Create a diamond shape (rotate a square)
diamond_size = 70
diamond_color = (233, 30, 99, 255)  # Pink color (#E91E63)

# Calculate diamond vertices
diamond_center = (width // 2, height // 2 - 10)  # Slightly above center
half_size = diamond_size // 2

# Diamond vertices (top, right, bottom, left)
diamond_vertices = [
    (diamond_center[0], diamond_center[1] - half_size),  # Top
    (diamond_center[0] + half_size, diamond_center[1]),  # Right
    (diamond_center[0], diamond_center[1] + half_size),  # Bottom
    (diamond_center[0] - half_size, diamond_center[1]),  # Left
]

draw.polygon(diamond_vertices, fill=diamond_color)

# Add text
try:
    # Try to use Arial font if available
    font = ImageFont.truetype("arial.ttf", 18)
except IOError:
    # Fallback to default font
    font = ImageFont.load_default()

text = "MetriBurn"
text_position = (width // 2, height // 2 + 55)
draw.text(text_position, text, fill=(255, 255, 255, 255), font=font, anchor="mm")

# Save the image as PNG
output_path = os.path.join(os.path.dirname(__file__), "metriburn_logo_new.png")
image.save(output_path, "PNG")

print(f"New logo saved to {output_path}")
