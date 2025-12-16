#!/usr/bin/env python3
"""
Analyze specific regions where screenshots differ
Identifies the exact areas that need CSS fixes
"""

from PIL import Image, ImageDraw, ImageFont
import numpy as np
from scipy import ndimage
import os

def analyze_diff_regions(original_path, reproduction_path, threshold=30):
    """
    Identify specific rectangular regions where images differ

    Returns detailed analysis of each different region
    """
    # Load images
    img1 = Image.open(original_path).convert('RGB')
    img2 = Image.open(reproduction_path).convert('RGB')

    if img1.size != img2.size:
        img2 = img2.resize(img1.size)

    # Calculate difference
    img1_array = np.array(img1)
    img2_array = np.array(img2)

    diff = np.abs(img1_array.astype(int) - img2_array.astype(int))
    diff_binary = np.any(diff > threshold, axis=2).astype(int)

    # Find connected regions
    labeled, num_features = ndimage.label(diff_binary)

    regions = []
    for i in range(1, num_features + 1):
        region_mask = labeled == i
        region_pixels = np.where(region_mask)

        if len(region_pixels[0]) < 1000:  # Skip tiny differences
            continue

        y_min, y_max = region_pixels[0].min(), region_pixels[0].max()
        x_min, x_max = region_pixels[1].min(), region_pixels[1].max()

        width = x_max - x_min
        height = y_max - y_min
        area = len(region_pixels[0])

        # Calculate average difference in this region
        region_diff = diff[region_mask]
        avg_diff = np.mean(region_diff)

        # Identify section based on Y position
        page_height = img1.size[1]
        y_center = (y_min + y_max) // 2

        if y_center < page_height * 0.15:
            section = "Header/Navigation"
        elif y_center < page_height * 0.25:
            section = "Hero Section"
        elif y_center < page_height * 0.45:
            section = "About Section"
        elif y_center < page_height * 0.60:
            section = "Services Section"
        elif y_center < page_height * 0.80:
            section = "Testimonials Section"
        else:
            section = "Footer"

        regions.append({
            'id': i,
            'section': section,
            'bbox': (x_min, y_min, width, height),
            'area': area,
            'center': ((x_min + x_max) // 2, y_center),
            'avg_diff': avg_diff,
            'severity': 'HIGH' if avg_diff > 100 else 'MEDIUM' if avg_diff > 50 else 'LOW'
        })

    # Sort by area (largest first)
    regions.sort(key=lambda r: r['area'], reverse=True)

    return regions

def visualize_regions(original_path, regions, output_path):
    """Draw bounding boxes around different regions"""
    img = Image.open(original_path).convert('RGB')
    draw = ImageDraw.Draw(img)

    colors = {
        'HIGH': (255, 0, 0),      # Red
        'MEDIUM': (255, 165, 0),  # Orange
        'LOW': (255, 255, 0)      # Yellow
    }

    for region in regions[:10]:  # Top 10 regions
        x, y, w, h = region['bbox']
        color = colors[region['severity']]

        # Draw rectangle
        draw.rectangle([x, y, x+w, y+h], outline=color, width=3)

        # Draw label
        label = f"{region['section']} ({region['severity']})"
        draw.text((x+5, y+5), label, fill=color)

    img.save(output_path)
    print(f"✓ Annotated image saved: {output_path}")

def main():
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    screenshots_dir = f'{base_path}/screenshots'

    pages = ['home', 'about', 'services']

    print("\n" + "="*70)
    print("DETAILED DIFF ANALYSIS")
    print("="*70)

    for page in pages:
        original = f'{screenshots_dir}/original_{page}.png'
        reproduction = f'{screenshots_dir}/reproduction_{page}.png'

        if not os.path.exists(original) or not os.path.exists(reproduction):
            continue

        print(f"\n{'='*70}")
        print(f"PAGE: {page.upper()}")
        print(f"{'='*70}\n")

        regions = analyze_diff_regions(original, reproduction)

        # Print top regions
        for i, region in enumerate(regions[:10], 1):
            x, y, w, h = region['bbox']
            print(f"{i}. {region['section']}")
            print(f"   Position: ({x}, {y})")
            print(f"   Size: {w}x{h} px")
            print(f"   Area: {region['area']:,} pixels")
            print(f"   Avg Difference: {region['avg_diff']:.1f}")
            print(f"   Severity: {region['severity']}")
            print()

        # Create annotated visualization
        visualize_regions(
            original,
            regions,
            f'{screenshots_dir}/annotated_{page}.png'
        )

    print("="*70)
    print("Analysis complete! Check annotated_*.png files for visual breakdown.")
    print("="*70)

if __name__ == "__main__":
    main()
