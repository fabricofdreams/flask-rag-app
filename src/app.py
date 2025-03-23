from flask import Flask, render_template, request, jsonify
import os
from utils.pdf_processor import process_pdf
from utils.rag import RAG
from config.settings import Config

app = Flask(__name__)
app.config.from_object(Config)

# Ensure PDF upload directory exists
os.makedirs(Config.PDF_UPLOAD_FOLDER, exist_ok=True)

# Inicializamos el sistema RAG
rag_system = RAG()

# Global variable to store Q&A history
QNA_HISTORY = []


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'pdf_files' not in request.files:
        return "No file part", 400

    files = request.files.getlist('pdf_files')
    if not files or files[0].filename == '':
        return "No selected files", 400

    processed_files = []
    for file in files:
        if file and file.filename.endswith('.pdf'):
            file_path = os.path.join(Config.PDF_UPLOAD_FOLDER, file.filename)
            file.save(file_path)

            # Procesar el PDF y añadirlo al sistema RAG
            text_data = process_pdf(file_path)
            rag_system.add_document(text_data)
            processed_files.append(file.filename)

    return render_template('results.html', processed_files=processed_files)


@app.route('/query', methods=['POST'])
def query():
    query = request.form.get('query')
    if not query:
        return jsonify({"error": "No query provided"}), 400

    response = rag_system.generate_response(query)
    # Store this Q&A in history
    QNA_HISTORY.append({"question": query, "answer": response})
    return jsonify({"response": response})


@app.route('/history')
def history():
    return render_template('history.html', qna_history=QNA_HISTORY)


if __name__ == '__main__':
    app.run(debug=app.config['DEBUG'])
