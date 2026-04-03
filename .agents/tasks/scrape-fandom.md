# Task: Multi-Source Scrape
**Objective**: Run spiders to collect fanfiction metadata for a specific keyword.

**Steps**:
1. Run `python3 spiders/webnovel_spider.py --keyword "{keyword}"`
2. Run `python3 spiders/ao3_spider.py --keyword "{keyword}"`
3. Verify JSON files exist in `data/raw/`.
4. Notify user of total novel count.
