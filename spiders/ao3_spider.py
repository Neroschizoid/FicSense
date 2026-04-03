import json
import time
import os
import argparse
from seleniumbase import Driver

def scrape_ao3(keyword):
    os.system("pkill -f chrome")
    driver = Driver(uc=True, headless2=True, driver_version="keep")
    results = []

    try:
        url = f"https://archiveofourown.org/works/search?work_search[query]={keyword}"
        driver.get(url)
        time.sleep(5)

        cards = driver.find_elements("css selector", "li.work.blurb")
        for card in cards:
            try:
                title_el = card.find_element("css selector", "h4.heading a:first-child")
                results.append({
                    "title": title_el.text.strip(),
                    "author": card.find_element("css selector", "a[rel='author']").text.strip(),
                    "synopsis": card.find_element("css selector", "blockquote.userstuff").text.strip(),
                    "link": title_el.get_attribute("href"),
                    "source": "AO3"
                })
            except: continue

        with open(f"data/raw/ao3_{keyword}.json", "w") as f:
            json.dump(results, f, indent=4)
        return len(results)
    finally:
        driver.quit()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--keyword", required=True)
    args = parser.parse_args()
    count = scrape_ao3(args.keyword)
    print(f"Captured {count} from AO3")
