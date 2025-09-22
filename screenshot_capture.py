import asyncio
import os
import math
import glob
import requests
from playwright.async_api import async_playwright
from dotenv import load_dotenv

load_dotenv()
FRONTEND_URL = os.getenv("FRONTEND_URL")

API_URL = "https://api.fellahedar.com/api/v1/product"
PAGE_SIZE = 6
OUTPUT_DIR = "screenshots"

def get_total_pages():
    params = {"page": 0, "size": PAGE_SIZE}
    response = requests.get(API_URL, params=params)
    response.raise_for_status()
    total_elements = response.json().get("totalElements", 0)
    return math.ceil(total_elements / PAGE_SIZE)

async def capture_screenshot(playwright, url: str, filename: str):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    save_path = os.path.join(OUTPUT_DIR, filename)

    browser = await playwright.chromium.launch(headless=True)
    context = await browser.new_context(
        viewport={"width": 390, "height": 730},
        device_scale_factor=3,
        is_mobile=True,
        has_touch=True,
        user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X)"
    )
    page = await context.new_page()
    await page.goto(url)
    await page.wait_for_timeout(1000)

    await page.screenshot(path=save_path, full_page=False)
    print(f"✅ Screenshot saved: {save_path}")
    await browser.close()

def clear_existing_screenshots():
    if os.path.exists(OUTPUT_DIR):
        image_patterns = ['*.png', '*.jpg', '*.jpeg', '*.gif', '*.bmp', '*.webp']
        deleted_count = 0
        
        for pattern in image_patterns:
            files = glob.glob(os.path.join(OUTPUT_DIR, pattern))
            for file_path in files:
                try:
                    os.remove(file_path)
                    print(f"✅ Deleted: {file_path}")
                    deleted_count += 1
                except OSError as e:
                    print(f"Error deleting {file_path}: {e}")
        
        if deleted_count > 0:
            print(f"Cleared {deleted_count} existing screenshot(s)")

async def main():
    clear_existing_screenshots()
    
    total_pages = get_total_pages()

    async with async_playwright() as playwright:
        for page_num in range(total_pages):
            frontend_url = f"{FRONTEND_URL}?page={page_num + 1}&size={PAGE_SIZE}"
            filename = f"story_page_{page_num + 1}.png"
            await capture_screenshot(playwright, frontend_url, filename)

if __name__ == "__main__":
    asyncio.run(main())
