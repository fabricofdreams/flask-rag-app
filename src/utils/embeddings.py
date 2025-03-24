from openai import OpenAI
from config.settings import Config

client = OpenAI(api_key=Config.OPENAI_API_KEY)


def preprocess_text(text):
    # Remueve espacios innecesarios y trunca a 8000 caracteres
    text = ' '.join(text.split())
    return text[:8000]


def generate_embeddings(text):
    try:
        preprocessed_text = preprocess_text(text)
        response = client.embeddings.create(
            input=preprocessed_text,
            model="text-embedding-ada-002"
        )
        return response.data[0].embedding
    except Exception as e:
        print(f"Error generando embeddings: {e}")
        return None
