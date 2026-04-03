# Spider Safety & Stealth Protocol
When managing or refactoring scripts in `/spiders`, follow these constraints:

1. **UC Mode Persistence**: Never remove `uc=True` or `headless2=True`. These are required to bypass Webnovel Cloudflare.
2. **Process Management**: Always include `os.system("pkill -f chrome")` before driver initialization to prevent zombie processes on the ASUS TUF hardware.
3. **Binary Paths**: Strictly use `/usr/bin/google-chrome` and `/usr/local/bin/chromedriver`.
4. **Error Handling**: If a scrape returns 0 results, do not hallucinate code changes; check if the site's CSS classes have changed in the Antigravity Browser view.
