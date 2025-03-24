import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'clave_secreta_por_defecto')
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY', 'tu_api_key_de_openai')
    PDF_UPLOAD_FOLDER = os.path.join(
        os.path.dirname(__file__), '..', 'data', 'pdfs')
    DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'
