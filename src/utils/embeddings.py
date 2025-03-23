from openai import OpenAI
from config.settings import Config
import numpy as np

client = OpenAI(api_key=Config.OPENAI_API_KEY)


def preprocess_text(text):
    """Preprocess the text before generating embeddings."""
    text = ' '.join(text.split())
    return text[:8000]


def generate_embeddings(text):
    """Generate embeddings using OpenAI's text-embedding-ada-002 model."""
    try:
        preprocessed_text = preprocess_text(text)
        response = client.embeddings.create(
            input=preprocessed_text,
            model="text-embedding-ada-002"
        )
        return response.data[0].embedding
    except Exception as e:
        print(f"Error generating embeddings: {e}")
        return None
