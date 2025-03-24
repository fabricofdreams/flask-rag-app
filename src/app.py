from flask import Flask, render_template, request, jsonify
from config.settings import Config
from utils.pdf_processor import process_pdf
from utils.rag import RAG
import os
import sys

# Definimos la ubicación base del proyecto (directorio raíz)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_DIR = os.path.join(BASE_DIR, "src")
# Agregamos la carpeta src al PYTHONPATH (esto debe hacerse antes de importar módulos de la raíz)
sys.path.insert(0, SRC_DIR)


# Definimos la ubicación base del proyecto (directorio raíz)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Agregamos el directorio raíz al PYTHONPATH (esto debe hacerse antes de importar módulos de la raíz)
sys.path.insert(0, BASE_DIR)


# Definimos las ubicaciones de los templates y archivos estáticos
TEMPLATE_DIR = os.path.join(BASE_DIR, "templates")
STATIC_DIR = os.path.join(BASE_DIR, "static")

app = Flask(__name__, template_folder=TEMPLATE_DIR, static_folder=STATIC_DIR)
app.config.from_object(Config)

# Aseguramos que el directorio para PDF exista
os.makedirs(Config.PDF_UPLOAD_FOLDER, exist_ok=True)

# Inicializamos el sistema RAG y el historial
rag_system = RAG()
QNA_HISTORY = []


@app.route('/')
def index():
    # Listamos los documentos subidos
    uploaded_files = os.listdir(Config.PDF_UPLOAD_FOLDER)
    return render_template("index.html", uploaded_files=uploaded_files)


@app.route('/upload', methods=["POST"])
def upload_file():
    if "pdf_files" not in request.files:
        return "No se encontró archivo", 400

    files = request.files.getlist("pdf_files")
    if not files or files[0].filename == "":
        return "No se seleccionó ningún archivo", 400

    for file in files:
        if file and file.filename.endswith(".pdf"):
            file_path = os.path.join(Config.PDF_UPLOAD_FOLDER, file.filename)
            file.save(file_path)
            text_data = process_pdf(file_path)
            rag_system.add_document(text_data)
    return render_template("index.html", uploaded_files=os.listdir(Config.PDF_UPLOAD_FOLDER))


@app.route('/query', methods=["POST"])
def query():
    query_text = request.form.get("query")
    if not query_text:
        return jsonify({"error": "No se proporcionó consulta"}), 400
    answer = rag_system.generate_response(query_text)
    QNA_HISTORY.append({"question": query_text, "answer": answer})
    return jsonify({"response": answer})


@app.route("/history")
def history():
    return render_template("history.html", qna_history=QNA_HISTORY)


if __name__ == "__main__":
    app.run(debug=app.config["DEBUG"])
