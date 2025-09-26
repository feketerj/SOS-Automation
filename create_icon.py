#!/usr/bin/env python3
"""
Creates a simple SOS icon for the desktop shortcut
"""

import os
try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    print("Installing required package...")
    os.system("pip install Pillow")
    from PIL import Image, ImageDraw, ImageFont

def create_sos_icon():
    # Create a 256x256 image with blue background
    size = 256
    img = Image.new('RGBA', (size, size), (0, 102, 204, 255))  # Nice blue color
    draw = ImageDraw.Draw(img)

    # Draw white circle in center
    margin = 20
    draw.ellipse([margin, margin, size-margin, size-margin],
                 fill=(255, 255, 255, 255))

    # Draw "SOS" text in blue
    try:
        # Try to use a nice font, fall back to default if not available
        font = ImageFont.truetype("arial.ttf", 72)
    except:
        font = ImageFont.load_default()

    text = "SOS"
    # Get text size for centering
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    # Center the text
    x = (size - text_width) // 2
    y = (size - text_height) // 2 - 10  # Slight upward adjustment

    draw.text((x, y), text, fill=(0, 102, 204, 255), font=font)

    # Save as ICO file with multiple sizes
    icon_sizes = [(16, 16), (32, 32), (48, 48), (256, 256)]
    img.save('SOS_Tool.ico', format='ICO', sizes=icon_sizes)

    print("Icon created: SOS_Tool.ico")
    print("To use it:")
    print("1. Right-click your desktop shortcut")
    print("2. Select Properties")
    print("3. Click 'Change Icon'")
    print("4. Browse to this file: SOS_Tool.ico")

    return "SOS_Tool.ico"

if __name__ == "__main__":
    icon_file = create_sos_icon()
    full_path = os.path.abspath(icon_file)
    print(f"\nFull path: {full_path}")