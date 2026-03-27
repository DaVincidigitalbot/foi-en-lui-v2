#!/usr/bin/env python3

from PIL import Image, ImageDraw, ImageFont
import numpy as np
import os

def create_gold_texture(width, height):
    """Create gold metallic texture"""
    np.random.seed(42)
    
    # Generate noise and streak patterns
    noise = np.random.normal(0, 20, (height, width)).astype(np.float32)
    streak = np.sin(np.arange(height).reshape(-1, 1) * 0.05) * 12
    
    # Create gold color channels
    r = np.clip(175 + noise + streak + np.random.randint(-10, 10, (height, width)), 90, 225).astype(np.uint8)
    g = np.clip(148 + noise * 0.8 + streak * 0.7, 70, 195).astype(np.uint8) 
    b = np.clip(72 + noise * 0.4 + streak * 0.3, 25, 130).astype(np.uint8)
    a = np.full((height, width), 255, dtype=np.uint8)
    
    # Stack channels
    texture = np.stack([r, g, b, a], axis=-1)
    return Image.fromarray(texture)

def create_text_mask(title, verse, width, height, font_path):
    """Create text mask for title and verse"""
    mask = Image.new('L', (width, height), 0)
    draw = ImageDraw.Draw(mask)
    
    # Load font - try different sizes
    title_font = None
    verse_font = None
    
    # Try to load fonts with appropriate sizes
    for size in [240, 220, 200, 180, 160, 140]:
        try:
            title_font = ImageFont.truetype(font_path, size)
            break
        except:
            continue
    
    for size in [120, 100, 90, 80, 70]:
        try:
            verse_font = ImageFont.truetype(font_path, size)
            break
        except:
            continue
    
    if not title_font or not verse_font:
        print(f"Warning: Could not load fonts, using default")
        title_font = ImageFont.load_default()
        verse_font = ImageFont.load_default()
    
    # Calculate text positions
    title_bbox = draw.textbbox((0, 0), title, font=title_font)
    title_width = title_bbox[2] - title_bbox[0]
    title_height = title_bbox[3] - title_bbox[1]
    title_x = (width - title_width) // 2
    title_y = height // 2 - title_height - 100
    
    verse_bbox = draw.textbbox((0, 0), verse, font=verse_font)
    verse_width = verse_bbox[2] - verse_bbox[0]
    verse_height = verse_bbox[3] - verse_bbox[1]
    verse_x = (width - verse_width) // 2
    verse_y = height // 2 + 50
    
    # Draw title
    draw.text((title_x, title_y), title, font=title_font, fill=255)
    
    # Draw flanking lines and verse
    line_length = 200
    line_y = verse_y + verse_height // 2
    left_line_start = verse_x - line_length - 50
    right_line_start = verse_x + verse_width + 50
    
    # Draw lines
    draw.line([(left_line_start, line_y), (left_line_start + line_length, line_y)], fill=255, width=8)
    draw.line([(right_line_start, line_y), (right_line_start + line_length, line_y)], fill=255, width=8)
    
    # Draw verse
    draw.text((verse_x, verse_y), verse, font=verse_font, fill=255)
    
    return mask

# Generate COURAGE back print
BASE_DIR = "/home/setup/.openclaw/workspace/products/foi-en-lui-v2"
title = "COURAGE"
verse = "Joshua 1:9"
filename = "courage"

print(f"Generating back print for: {title}")

# Create high-res version first
WIDTH, HEIGHT = 4500, 5400

# Create gold texture
texture_img = create_gold_texture(WIDTH, HEIGHT)

# Create text mask
font_path = "/tmp/AllertaStencil.ttf"
mask = create_text_mask(title, verse, WIDTH, HEIGHT, font_path)

# Apply mask to texture
result = Image.new('RGBA', (WIDTH, HEIGHT), (0, 0, 0, 0))
result.paste(texture_img, mask=mask)

# Resize to web-ready size (800x800)
web_size = result.resize((800, 800), Image.Resampling.LANCZOS)

# Save the web-ready version
output_path = os.path.join(BASE_DIR, f"back-{filename}.png")
web_size.save(output_path, "PNG")
print(f"Saved: {output_path}")