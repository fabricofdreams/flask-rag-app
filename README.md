# README.md

# Flask RAG App

A Flask application implementing a Retrieval Augmented Generation (RAG) system. This app allows users to upload PDF files, processes and indexes their content, and then answers queries using OpenAI's GPT-4 in combination with document embeddings.

## Features

- **PDF Upload**: Upload one or more PDF documents.
- **Document Processing**: Extracts text from PDFs and generates embeddings.
- **Query Interface**: Ask questions based on the uploaded documents.
- **RAG**: Combines retrieval of relevant document excerpts with GPT-4 to answer queries.
- **Responsive Design**: Modern and clean user interface with navigation.

## Technologies

- Python 3.9+
- Flask
- OpenAI API (using the new client-based interface)
- PyPDF2 for PDF processing
- Scikit-learn for similarity computations
- tiktoken for token counting and context truncation
- python-dotenv for environment configuration
- Gunicorn for production

## Setup Instructions

1. **Clone the repository:**

   ```bash
   git clone <repository-url>
   cd flask-rag-app
   ```

2. **Create and activate a virtual environment (using conda is recommended):**

   ```bash
   conda create -n rag-env python=3.9
   conda activate rag-env
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Variables:**

   Create a `.env` file in the project root with the following variables:

   ```dotenv
   OPENAI_API_KEY=your_openai_api_key_here
   SECRET_KEY=your_secret_key_here
   DEBUG=True
   ```

5. **Prepare the File Upload Directory:**

   Ensure the PDF upload folder exists:

   ```bash
   mkdir -p data/pdfs
   chmod 755 data/pdfs
   ```

## Running the Application

For development, run:

```bash
python src/app.py
```

Then, open your browser and navigate to [http://127.0.0.1:5000](http://127.0.0.1:5000).

## Deployment

For production deployments, consider using Gunicorn. For instance:

```bash
gunicorn --bind 0.0.0.0:8000 wsgi:app
```

(Ensure you create a `wsgi.py` file to expose your Flask app.)

## Folder Structure

```
flask-rag-app/
├── data/
│   └── pdfs/        # Directory for uploaded PDFs
├── src/
│   ├── app.py       # Main Flask application
│   ├── config/
│   │   └── settings.py    # Application configuration
│   ├── templates/   # HTML templates
│   |   ├── base.html
│   |   └── index.html
│   ├── static/      # Static files (CSS, JS)
│   └── utils/       # Utility modules (RAG, embeddings, PDF processing)
├── .env             # Environment configuration
├── .gitignore
├── requirements.txt
└── README.md
```

## Contributing

Contributions are welcome! Please submit pull requests or raise issues if you have suggestions or bug fixes.

## License

[Insert license information here, if applicable]

---

Happy coding!
