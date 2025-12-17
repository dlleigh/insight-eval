#!/usr/bin/env python3
"""
Screenshot Capture Script for Website Comparison
Captures screenshots of both original and reproduction sites
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import os

def capture_screenshot(url, output_path, width=1920, height=3000):
    """
    Capture a screenshot of a webpage at specified dimensions

    Args:
        url: URL or file path to capture
        output_path: Where to save the screenshot
        width: Viewport width in pixels
        height: Viewport height in pixels
    """
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--hide-scrollbars')
    options.add_argument(f'--window-size={width},{height}')
    options.add_argument('--force-device-scale-factor=1')  # Disable DPI scaling
    options.add_argument('--disable-cache')  # Force fresh CSS/JS loading
    options.add_argument('--disk-cache-size=0')  # Disable disk cache

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    try:
        print(f"Loading: {url}")
        driver.get(url)

        # Wait for page to fully load
        time.sleep(3)

        # Ensure directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        # Capture screenshot
        driver.save_screenshot(output_path)
        print(f"✓ Screenshot saved: {output_path}")

    except Exception as e:
        print(f"✗ Error capturing {url}: {e}")

    finally:
        driver.quit()


def main():
    """Capture screenshots of all pages"""

    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    pages = [
        ('home', '', 'index.html'),
        ('about', 'about-us', 'about-us.html'),
        ('services', 'services', 'services.html'),
    ]

    print("=" * 60)
    print("CAPTURING SCREENSHOTS")
    print("=" * 60)

    for name, url_path, file_name in pages:
        print(f"\n[{name.upper()}]")

        # Original site
        original_url = f'https://insighteval.com/{url_path}' if url_path else 'https://insighteval.com/'
        capture_screenshot(
            original_url,
            f'{base_path}/screenshots/original_{name}.png'
        )

        # Reproduction
        local_url = f'file://{base_path}/{file_name}'
        capture_screenshot(
            local_url,
            f'{base_path}/screenshots/reproduction_{name}.png'
        )

    print("\n" + "=" * 60)
    print("SCREENSHOT CAPTURE COMPLETE")
    print("=" * 60)
    print(f"\nScreenshots saved to: {base_path}/screenshots/")


if __name__ == "__main__":
    main()
