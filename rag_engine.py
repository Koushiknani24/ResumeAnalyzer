import json
import os
import google.generativeai as genai
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import streamlit as st

class RAGEngine:
    def __init__(self, kb_path="data/rag_knowledge_base.json"):
        self.kb_path = kb_path
        self.knowledge_base = []
        self.embeddings = []
        self.is_initialized = False
        
        # Configure Gemini
        try:
            api_key = st.secrets["GEMINI_API_KEY"]
            genai.configure(api_key=api_key)
        except KeyError:
            print("GEMINI_API_KEY not found in secrets. RAG Engine might fail.")
            
    def initialize(self):
        """Loads the JSON and generates embeddings for all items."""
        if not os.path.exists(self.kb_path):
            print(f"RAG Knowledge base not found at {self.kb_path}")
            return
            
        with open(self.kb_path, 'r') as f:
            self.knowledge_base = json.load(f)
            
        # We will embed the 'content' + 'example' of each item to create a rich vector representation
        texts_to_embed = [f"{item['content']} {item.get('example', '')}" for item in self.knowledge_base]
        
        try:
            # Use Gemini's embedding model
            result = genai.embed_content(
                model="models/text-embedding-004",
                content=texts_to_embed,
                task_type="retrieval_document"
            )
            
            # genai.embed_content returns a dictionary with 'embedding' key containing a list of vectors
            if isinstance(result, dict) and 'embedding' in result:
                self.embeddings = np.array(result['embedding'])
            else:
                 # Fallback if structure is different
                 self.embeddings = np.array([res['embedding'] for res in result])
                 
            self.is_initialized = True
        except Exception as e:
            print(f"Error initializing RAG embeddings: {e}")

    def query(self, query_text: str, top_k: int = 2) -> list:
        """Embeds the query and returns the top_k most similar items from the knowledge base."""
        if not self.is_initialized:
            self.initialize()
            
        if not self.is_initialized or len(self.embeddings) == 0:
            return []
            
        try:
            query_result = genai.embed_content(
                model="models/text-embedding-004",
                content=query_text,
                task_type="retrieval_query"
            )
            
            if isinstance(query_result, dict) and 'embedding' in query_result:
                query_vector = np.array(query_result['embedding']).reshape(1, -1)
            else:
                query_vector = np.array(query_result['embedding']).reshape(1, -1)
                
            # Calculate cosine similarity
            similarities = cosine_similarity(query_vector, self.embeddings)[0]
            
            # Get top_k indices
            top_indices = np.argsort(similarities)[-top_k:][::-1]
            
            results = []
            for idx in top_indices:
                if similarities[idx] > 0.3: # Threshold to ensure relevance
                    item = self.knowledge_base[idx].copy()
                    item['similarity_score'] = float(similarities[idx])
                    results.append(item)
                    
            return results
        except Exception as e:
            print(f"Error querying RAG: {e}")
            return []

# Singleton instance
rag_engine = RAGEngine()
