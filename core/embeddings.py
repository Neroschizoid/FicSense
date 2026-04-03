import ollama
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from config import Config

def get_embeddings(texts):
    """Batch processes a list of strings into vectors using the configured Ollama model."""
    print(f"🧠 [FicSense] Generating embeddings for {len(texts)} items...")
    
    # nomic-embed-text performs better with 'search_document:' prefix for stored content
    formatted_texts = [f"search_document: {t}" for t in texts]
    
    # Call Ollama using the model defined in Config
    response = ollama.embed(model=Config.EMBED_MODEL, input=formatted_texts)
    return np.array(response['embeddings'])

def get_query_vector(query):
    """Converts the user intent into a search vector using the 'search_query:' prefix."""
    response = ollama.embed(model=Config.EMBED_MODEL, input=f"search_query: {query}")
    return np.array(response['embeddings'][0]).reshape(1, -1)

def rank_novels(query, novels, top_n=15):
    """Ranks novels based on semantic cosine similarity to the user's intent."""
    if not novels:
        print("⚠️ No novels provided for ranking.")
        return []

    # 1. Prepare text for embedding (Title + Synopsis)
    # We combine them so the model understands context from both
    descriptions = [f"{n['title']} {n['synopsis']}" for n in novels]
    
    # 2. Vectorize Documents and Query
    try:
        doc_vectors = get_embeddings(descriptions)
        query_vector = get_query_vector(query)
    except Exception as e:
        print(f"❌ Ollama Embedding Error: {e}")
        return []

    # 3. Calculate Cosine Similarity
    # This results in a list of scores (usually 0.5 to 0.9 for related text)
    scores = cosine_similarity(query_vector, doc_vectors)[0]

    # 4. Attach scores and sort by highest relevance
    for i, novel in enumerate(novels):
        novel["score"] = float(scores[i])

    ranked = sorted(novels, key=lambda x: x["score"], reverse=True)
    
    print(f"✅ Ranked {len(ranked)} items. Returning top {top_n}.")
    return ranked[:top_n]