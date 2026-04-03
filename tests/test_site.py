from core.embeddings import rank_novels

def test_time_travel_intent():
    mock_novels = [
        {"title": "The Temporal Anchor", "synopsis": "A hero goes back to the past to save his friends.", "link": "1"},
        {"title": "Gourmet Chef", "synopsis": "A story about a man cooking delicious food in a small shop.", "link": "2"},
        {"title": "Rewinding the Clock", "synopsis": "Waking up in his 10-year-old body, he decides to change everything.", "link": "3"},
        {"title": "Sword God", "synopsis": "Becoming the strongest swordsman in the world through hard work.", "link": "4"}
    ]
    
    intent = "time travel back to the past and redo life"
    results = rank_novels(intent, mock_novels, top_n=2)
    
    print(f"Intent: {intent}")
    for r in results:
        print(f"Matched: {r['title']} - Score: {r['score']:.4f}")

    # Check if 'The Temporal Anchor' or 'Rewinding the Clock' are in top 2
    top_titles = [r['title'] for r in results]
    assert "The Temporal Anchor" in top_titles or "Rewinding the Clock" in top_titles
    assert "Gourmet Chef" not in top_titles

if __name__ == "__main__":
    print("🧪 Testing Semantic Intent Engine...")
    try:
        test_time_travel_intent()
        print("✅ TEST PASSED: Model understands 'Time Travel' semantics.")
    except Exception as e:
        print(f"❌ TEST FAILED: {e}")