import json
import time
import os
import argparse
from seleniumbase import Driver
from config import Config

def scrape_webnovel(keyword, scrolls=Config.DEFAULT_SCROLLS):
    # 1. Kill zombie processes to keep the ASUS TUF stable
    os.system("pkill -f chrome")
    
    # 2. Force environment variables from our Central Config
    os.environ["CHROME_BINARY"] = Config.CHROME_BINARY
    os.environ["webdriver.chrome.driver"] = Config.CHROME_DRIVER
    
    print(f"🌐 [FicSense] Opening Webnovel Window for: {keyword}")
    
    # --- VISIBLE MODE ---
    # Configured via central config and stealth-patched for Cloudflare
    driver = Driver(uc=True, headless=False, driver_version="keep")
    results = []

    try:
        url = f"https://www.webnovel.com/search?keywords={keyword}&type=fanfic"
        driver.uc_open_with_reconnect(url, 6)
        
        # In case you need to manually click a captcha in the window
        driver.uc_gui_click_captcha()

        print("⏳ Waiting for initial page load (10s)...")
        time.sleep(10) 

        # --- SCROLLING LOGIC ---
        for i in range(scrolls):
            print(f"  ⬇️ Scrolling {i+1}/{scrolls}...")
            driver.execute_script("window.scrollBy(0, 2000);")
            time.sleep(3) 

        print("📊 Extracting DOM metadata...")
        
        # Target the list items from your specific successful run
        items = driver.find_elements("css selector", "li.pr.pb20.mb12")
        
        for item in items:
            try:
                title_el = item.find_element("css selector", "h3 a")
                name = title_el.get_attribute("title")
                path = title_el.get_attribute("href")
                
                # Metadata extraction
                try:
                    desc = item.find_element("css selector", "p[class*='lh24']").text.strip()
                except:
                    desc = "No synopsis found."

                try:
                    # Look for author profile link
                    author = item.find_element("css selector", "a[href*='/profile/']").text.strip()
                except:
                    author = "N/A"

                if name:
                    results.append({
                        "title": name,
                        "author": author,
                        "synopsis": desc,
                        "link": f"https://www.webnovel.com{path}" if path.startswith("/") else path,
                        "source": "Webnovel"
                    })
            except Exception:
                continue
            
        # Save locally using path from Config
        os.makedirs(Config.RAW_DATA_DIR, exist_ok=True)
        output_file = os.path.join(Config.RAW_DATA_DIR, f"webnovel_{keyword}.json")
        
        with open(output_file, "w") as f:
            json.dump(results, f, indent=4)
            
        return results # Returning the list for the bot/pipeline to consume

    finally:
        print("\n🏁 Scrape finished. Closing window in 5 seconds...")
        time.sleep(5)
        driver.quit()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--keyword", required=True)
    args = parser.parse_args()
    
    # Ensure driver is executable using Config path
    os.system(f"sudo chmod +x {Config.CHROME_DRIVER}")
    
    novel_list = scrape_webnovel(args.keyword)
    print(f"\n✅ FicSense SUCCESS: Captured {len(novel_list)} novels.")