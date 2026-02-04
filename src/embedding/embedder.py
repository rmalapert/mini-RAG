# src/embedding/embedder.py

class Chunk:
    def __init__(self, text, document_name):
        self.text = text
        self.document_name = document_name

class VectorEmbedding:
    def __init__(self, values, chunk):
        self.values = values  # Liste de float
        self.chunk = chunk    # Instance de Chunk
