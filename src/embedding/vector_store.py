from pymilvus import connections, FieldSchema, CollectionSchema, DataType, Collection
import numpy as np
import uuid
import os
import sys
from typing import List
 
from pymilvus import MilvusClient
from src.embedding.embedder import VectorEmbedding
 
 
class VectorStore:
    def __init__(self, dim, collection_name="milvus"):
        self.collection_name = collection_name
 
        # 1. Creates db
        self.client = MilvusClient("milvus.db")
 
        # 2. Structure de la collection
        schema = CollectionSchema(
            fields=[
                FieldSchema(name="id", dtype=DataType.VARCHAR, is_primary=True, auto_id=False, max_length=36),
                FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=dim),
                FieldSchema(name="document_name", dtype=DataType.VARCHAR, max_length=10000),
                FieldSchema(name="text", dtype=DataType.VARCHAR, max_length=10000),
            ],
            description="Collection pour stocker les embeddings des chunks",
        )
 
        # 3. Create index parameters
        index_params = self.client.prepare_index_params()
 
        index_params.add_index(
            field_name="embedding",
            index_type="IVF_FLAT",
            metric_type="COSINE",
            params={"nlist": 1024}
        )
       
        # 4. Create a collection
        if self.client.has_collection(collection_name):
            self.client.drop_collection(collection_name)
        self.client.create_collection(
            collection_name=collection_name,
            schema=schema
        )
 
        # 5. Create indexes
        self.client.create_index(
            collection_name=collection_name,
            index_params=index_params,
            sync=False
        )
 
    def add_chunks(self, embeddings: List[VectorEmbedding]):
        """Ajoute des chunks et leurs embeddings à Milvus.
        Args:
            embeddings (List[List[float]]): Liste des vecteurs embeddings.
        """
        ids = [str(uuid.uuid4()) for _ in embeddings]
        data = [{
            "id": ids[i],
            "embedding": embeddings[i].values,
            "text": embeddings[i].chunk.text,
            "document_name": embeddings[i].chunk.document_name
        } for i in range(len(ids))]
        self.client.insert(self.collection_name, data)
 
    def search(self, query_embedding, top_k=5):
        """Recherche les chunks les plus similaires à la requete.
        Args:
            query_embedding (List[float]): L'embedding à rechercher.
            top_k (int): Nombre de résultats à retourner.
        Returns:
            List[Tuple[str, float]]: Paires (texte, score de distance).
        """
        results = self.client.search(
            collection_name=self.collection_name,
            data=[query_embedding[0].values],
            anns_field="embedding",
            limit=top_k,
            output_fields=["text"]
        )
 
        matches = [hit.entity.get("text") for hit in results[0]]
        return matches