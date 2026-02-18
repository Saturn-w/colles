#!/usr/bin/env python3
"""Generate PWA icons from SVG"""

from PIL import Image, ImageDraw, ImageFont
import os


def create_icon(size, filename):
    """Create a simple icon with PIL"""
    # Create image with dark background
    img = Image.new("RGBA", (size, size), (15, 15, 15, 255))
    draw = ImageDraw.Draw(img)

    # Draw blue document shape
    margin = size // 6
    doc_width = size - 2 * margin
    doc_height = int(doc_width * 1.35)
    doc_x = margin
    doc_y = (size - doc_height) // 2

    # Blue rectangle with rounded corners
    draw.rounded_rectangle(
        [(doc_x, doc_y), (doc_x + doc_width, doc_y + doc_height)],
        radius=size // 20,
        fill=(52, 152, 219, 255),
    )

    # Darker header
    draw.rounded_rectangle(
        [(doc_x, doc_y), (doc_x + doc_width, doc_y + doc_height // 4)],
        radius=size // 20,
        fill=(41, 128, 185, 255),
    )

    # Text lines
    line_margin = doc_x + size // 10
    line_width = doc_width - size // 5
    line_y_start = doc_y + doc_height // 3
    line_spacing = size // 15

    for i in range(3):
        y = line_y_start + i * line_spacing
        line_length = line_width if i < 2 else line_width * 0.7
        draw.rounded_rectangle(
            [(line_margin, y), (line_margin + line_length, y + size // 60)],
            radius=size // 120,
            fill=(224, 224, 224, 255),
        )

    # Try to add PSI text
    try:
        # Use default font, scaled to size
        font_size = size // 8
        font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", font_size)
    except:
        font = ImageFont.load_default()

    # Draw PSI text
    text = "PSI"
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    text_x = doc_x + (doc_width - text_width) // 2
    text_y = doc_y + (doc_height // 8) - text_height // 2

    draw.text((text_x, text_y), text, fill=(255, 255, 255, 255), font=font)

    # Save
    img.save(filename, "PNG")
    print(f"✓ Created {filename}")


if __name__ == "__main__":
    create_icon(192, "icon-192.png")
    create_icon(512, "icon-512.png")
    print("All icons created successfully!")
