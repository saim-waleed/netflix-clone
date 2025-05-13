from PIL import Image, ImageDraw, ImageFont
import os

def create_placeholder(filename, width, height, text, bg_color=(229, 9, 20), text_color=(255, 255, 255)):
    # Create a new image with a solid background
    image = Image.new('RGB', (width, height), bg_color)
    draw = ImageDraw.Draw(image)
    
    # Calculate text size and position
    text_width = draw.textlength(text, font=None)
    text_x = (width - text_width) // 2
    text_y = (height - 10) // 2
    
    # Draw text
    draw.text((text_x, text_y), text, fill=text_color)
    
    # Save the image
    image.save(os.path.join('static/images', filename))

# Create images directory if it doesn't exist
os.makedirs('static/images', exist_ok=True)

# Create placeholder images
placeholders = [
    ('netflix-logo.png', 200, 80, 'NETFLIX'),
    ('avatar.png', 32, 32, 'User'),
    ('featured-thumbnail.jpg', 1280, 720, 'Featured Movie'),
    ('movie1.jpg', 300, 169, 'Movie 1'),
    ('movie2.jpg', 300, 169, 'Movie 2'),
    ('movie3.jpg', 300, 169, 'Movie 3'),
]

for filename, width, height, text in placeholders:
    create_placeholder(filename, width, height, text)

print("Placeholder images created successfully!") 