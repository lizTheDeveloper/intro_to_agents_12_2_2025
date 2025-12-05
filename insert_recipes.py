# Requires sentence-transformers>=2.7.0

from sentence_transformers import SentenceTransformer

# Load the model
model = SentenceTransformer("Qwen/Qwen3-Embedding-0.6B")

recipe_file = open("recipes/example.cook").read()


document_embeddings = model.encode(recipe_file)
import numpy as np
document_embeddings = np.array(document_embeddings).astype(np.float16)



import psycopg2
import os
conn = psycopg2.connect(
    os.getenv("DATABASE_URL")
)
cursor = conn.cursor()
cursor.execute("INSERT INTO recipes (embedding, recipe_text) VALUES (%s, %s)", (document_embeddings.tolist(), recipe_file))
conn.commit()
cursor.close()
conn.close()