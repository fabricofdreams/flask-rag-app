from openai import OpenAI
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from .embeddings import generate_embeddings
from config.settings import Config
import tiktoken  # type: ignore


class RAG:
    def __init__(self):
        self.document_embeddings = []
        self.documents = []
        self.client = OpenAI(api_key=Config.OPENAI_API_KEY)
        self.model = "gpt-4"
        self.tokenizer = tiktoken.encoding_for_model(self.model)
        self.max_context_tokens = 6000  # Reserve tokens for system prompt and response
        self.max_response_tokens = 1000

    def count_tokens(self, text):
        """Count the number of tokens in a text."""
        try:
            return len(self.tokenizer.encode(text))
        except Exception as e:
            print(f"Error counting tokens: {e}")
            return 0

    def truncate_context(self, context, available_tokens):
        """Truncate context to fit within available tokens."""
        tokens = self.tokenizer.encode(context)
        if len(tokens) <= available_tokens:
            return context
        return self.tokenizer.decode(tokens[:available_tokens])

    def add_document(self, text):
        embedding = generate_embeddings(text)
        if embedding:
            self.document_embeddings.append(embedding)
            self.documents.append(text)

    def find_relevant_context(self, query_embedding, top_k=3):
        """Find and return the most relevant context within token limits."""
        if not self.document_embeddings:
            return ""

        # Calculate similarities
        similarities = [
            cosine_similarity([query_embedding], [doc_emb])[0][0]
            for doc_emb in self.document_embeddings
        ]

        # Get top k most similar documents
        top_indices = np.argsort(similarities)[-top_k:][::-1]
        relevant_docs = [self.documents[i] for i in top_indices]

        # Combine and truncate context
        context = "\n\n".join(relevant_docs)
        return self.truncate_context(context, self.max_context_tokens)

    def generate_response(self, query):
        query_embedding = generate_embeddings(query)
        if not query_embedding:
            return "Error generando la consulta."

        # Obtiene el contexto relevante de los documentos
        context = self.find_relevant_context(query_embedding)

        # Mensaje del sistema que indica el rol y uso del contexto
        system_prompt = (
            "Eres un asistente experto en documentos. "
            "El siguiente contexto corresponde al contenido extraído de los archivos PDF subidos. "
            "Utiliza este contexto para responder de manera precisa a la pregunta. "
            "Si el contexto está vacío, informa que no se encontró información relevante."
        )

        query_with_context = f"Contexto: {context}\n\nPregunta: {query}"

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": query_with_context}
                ],
                max_tokens=self.max_response_tokens,
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error generando la respuesta: {str(e)}"
