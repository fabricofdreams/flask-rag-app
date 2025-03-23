import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your_default_secret_key'
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY') or 'your_openai_api_key'
    MODEL_NAME = 'gpt-4'
    PDF_UPLOAD_FOLDER = os.path.join(os.path.dirname(
        os.path.dirname(os.path.dirname(__file__))), 'data', 'pdfs')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # Limit upload size to 16 MB
    DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'
