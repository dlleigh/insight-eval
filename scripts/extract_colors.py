#!/usr/bin/env python3
"""
Extract dominant colors from original screenshots
Helps identify exact color values used in original design
"""

from PIL import Image
import numpy as np
from collections import Counter
import os

def rgb_to_hex(rgb):
    """Convert RGB tuple to hex color"""
    return f"#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}"

def extract_colors_from_region(image_path, x, y, width, height, top_n=5):
    """Extract most common colors from a specific region"""
    img = Image.open(image_path).convert('RGB')

    # Crop to region
    region = img.crop((x, y, x + width, y + height))

    # Get all pixels
    pixels = np.array(region)
    pixels_flat = pixels.reshape(-1, 3)

    # Count occurrences
    pixel_tuples = [tuple(pixel) for pixel in pixels_flat]
    color_counts = Counter(pixel_tuples)

    # Get top colors
    top_colors = color_counts.most_common(top_n)

    return [(rgb, count, rgb_to_hex(rgb)) for rgb, count in top_colors]

def analyze_page_colors(image_path, page_name):
    """Analyze colors in different sections of the page"""
    img = Image.open(image_path)
    width, height = img.size

    print(f"\n{'='*70}")
    print(f"COLOR ANALYSIS: {page_name.upper()}")
    print(f"{'='*70}\n")

    # Define regions to analyze
    regions = {
        'Services Section Background': (0, int(height * 0.47), width, int(height * 0.57)),
        'Footer Background': (0, int(height * 0.89), width, height),
        'Hero Section': (0, int(height * 0.05), width, int(height * 0.15)),
        'Body Text Area': (int(width * 0.3), int(height * 0.35), int(width * 0.7), int(height * 0.40)),
    }

    for region_name, (x, y, x2, y2) in regions.items():
        w = x2 - x
        h = y2 - y

        print(f"\n{region_name}:")
        print(f"  Region: ({x}, {y}) to ({x2}, {y2})")

        try:
            colors = extract_colors_from_region(image_path, x, y, w, h, top_n=3)

            for i, (rgb, count, hex_color) in enumerate(colors, 1):
                percentage = (count / (w * h)) * 100
                print(f"  {i}. {hex_color} - RGB{rgb} - {percentage:.1f}% coverage")
        except Exception as e:
            print(f"  Error: {e}")

def main():
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    screenshots_dir = f'{base_path}/screenshots'

    pages = ['home', 'about', 'services']

    print("\n" + "="*70)
    print("EXTRACTING EXACT COLORS FROM ORIGINAL SITE")
    print("="*70)

    for page in pages:
        original = f'{screenshots_dir}/original_{page}.png'

        if not os.path.exists(original):
            print(f"\n⚠ Skipping {page}: Screenshot not found")
            continue

        analyze_page_colors(original, page)

    print("\n" + "="*70)
    print("COLOR EXTRACTION COMPLETE")
    print("="*70)
    print("\nUse these exact hex values in your CSS to match the original!")

if __name__ == "__main__":
    main()
