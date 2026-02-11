from sentence_transformers import SentenceTransformer

# Small, fast model (NO API key required)
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

def generate_embedding(text: str):
    try:
        return model.encode(text).tolist()
    except Exception as e:
        print("Embedding API failed:", e)
        return [0.0] * 384
