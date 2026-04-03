import sys
import os
import json
from spiders.webnovel_spider import scrape_webnovel
from core.embeddings import rank_novels
from config import Config

def run_ficsense_pipeline(keyword, intent):
    """The master sequence: Scrape -> Rank -> Return."""
    print(f"🚀 [FicSense] Processing: {keyword} | Intent: {intent}")
    
    # 1. Trigger the Visible Spider
    # Returns the list of novels directly from the function
    novels = scrape_webnovel(keyword, scrolls=Config.DEFAULT_SCROLLS)
    
    if not novels or len(novels) == 0:
        print("⚠️ No novels captured. Check Chrome window for blocks.")
        return []

    # 2. Semantic Ranking via Ollama
    print(f"🧠 Ranking {len(novels)} novels against intent: '{intent}'")
    top_matches = rank_novels(intent, novels, top_n=15)

    # 3. Return the ranked results to the caller (Bot or CLI)
    return top_matches

if __name__ == "__main__":
    # Fallback for CLI testing: python3 main.py onepiece "time travel"
    fandom = sys.argv[1] if len(sys.argv) > 1 else "onepiece"
    user_intent = sys.argv[2] if len(sys.argv) > 2 else "time travel"
    
    results = run_ficsense_pipeline(fandom, user_intent)
    for i, res in enumerate(results, 1):
        print(f"{i}. {res['title']} - Score: {res['score']:.4f}")