#!/usr/bin/env python3
"""
Screenshot Comparison Script
Compares original vs reproduction screenshots pixel-by-pixel
"""

from PIL import Image, ImageChops, ImageDraw, ImageFont
import numpy as np
import os

def compare_images(image1_path, image2_path, output_path='screenshots/diff.png', threshold=30):
    """
    Compare two images and generate a diff highlighting differences

    Args:
        image1_path: Path to first image (original)
        image2_path: Path to second image (reproduction)
        output_path: Where to save the diff image
        threshold: Pixel difference threshold (0-255)

    Returns:
        Dictionary with comparison metrics
    """
    # Load images
    img1 = Image.open(image1_path).convert('RGB')
    img2 = Image.open(image2_path).convert('RGB')

    # Ensure same size
    if img1.size != img2.size:
        print(f"⚠ Warning: Image sizes differ. Resizing to match.")
        print(f"  Image 1: {img1.size}")
        print(f"  Image 2: {img2.size}")
        img2 = img2.resize(img1.size, Image.Resampling.LANCZOS)

    # Calculate difference
    diff = ImageChops.difference(img1, img2)

    # Convert to numpy for analysis
    diff_array = np.array(diff)

    # Calculate metrics
    total_pixels = diff_array.shape[0] * diff_array.shape[1]
    different_pixels = np.count_nonzero(np.any(diff_array > threshold, axis=-1))
    difference_percentage = (different_pixels / total_pixels) * 100

    # Create visual diff (highlight differences in red)
    diff_visual = img1.copy()
    diff_highlight = Image.new('RGB', img1.size, (255, 0, 0))

    # Create mask from differences
    mask = diff.convert('L').point(lambda x: 255 if x > threshold else 0)

    # Blend red highlight over original where differences exist
    diff_visual.paste(diff_highlight, (0, 0), mask)

    # Ensure directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Save diff image
    diff_visual.save(output_path)

    # Return metrics
    results = {
        'total_pixels': total_pixels,
        'different_pixels': different_pixels,
        'difference_percentage': difference_percentage,
        'threshold': threshold,
        'diff_image': output_path
    }

    return results


def print_results(name, results):
    """Pretty print comparison results"""
    print("\n" + "=" * 60)
    print(f"COMPARISON RESULTS: {name.upper()}")
    print("=" * 60)
    print(f"Total Pixels:      {results['total_pixels']:,}")
    print(f"Different Pixels:  {results['different_pixels']:,}")
    print(f"Difference:        {results['difference_percentage']:.3f}%")
    print(f"Threshold:         {results['threshold']}")
    print(f"Diff Image:        {results['diff_image']}")
    print("=" * 60)

    # Interpretation
    if results['difference_percentage'] < 1:
        print("✅ EXCELLENT: <1% difference - Nearly pixel-perfect!")
    elif results['difference_percentage'] < 5:
        print("✓ GOOD: <5% difference - Minor discrepancies")
    elif results['difference_percentage'] < 10:
        print("⚠ FAIR: 5-10% difference - Noticeable differences")
    else:
        print("❌ NEEDS WORK: >10% difference - Significant differences")


def main():
    """Compare all captured screenshots"""

    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    screenshots_dir = f'{base_path}/screenshots'

    pages = ['home', 'about', 'services']

    print("\n" + "=" * 60)
    print("COMPARING SCREENSHOTS")
    print("=" * 60)

    all_results = {}

    for page in pages:
        original = f'{screenshots_dir}/original_{page}.png'
        reproduction = f'{screenshots_dir}/reproduction_{page}.png'
        diff_output = f'{screenshots_dir}/diff_{page}.png'

        # Check if files exist
        if not os.path.exists(original):
            print(f"\n⚠ Skipping {page}: Original screenshot not found")
            continue

        if not os.path.exists(reproduction):
            print(f"\n⚠ Skipping {page}: Reproduction screenshot not found")
            continue

        # Compare
        results = compare_images(original, reproduction, diff_output)
        all_results[page] = results

        # Print results
        print_results(page, results)

    # Summary
    if all_results:
        print("\n" + "=" * 60)
        print("SUMMARY")
        print("=" * 60)

        for page, results in all_results.items():
            status = "✅" if results['difference_percentage'] < 1 else \
                     "✓" if results['difference_percentage'] < 5 else \
                     "⚠" if results['difference_percentage'] < 10 else "❌"

            print(f"{status} {page.upper():12} {results['difference_percentage']:6.3f}% difference")

        avg_diff = sum(r['difference_percentage'] for r in all_results.values()) / len(all_results)
        print("=" * 60)
        print(f"Average Difference: {avg_diff:.3f}%")
        print("=" * 60)


if __name__ == "__main__":
    main()
