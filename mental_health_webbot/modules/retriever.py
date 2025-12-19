import faiss
import numpy as np
import pickle
import os
from sentence_transformers import SentenceTransformer
import logging
from typing import list, dict
from modules.web_scraper import WebScraper

logger = logging.getLogger(__name__)

class AdvancedRetriever:
    """Retrieve relevant information using FAISS + web scraping."""
    
    def __init__(self, faiss_index_path: str = None, chunks_path: str = None):
        """Initialize retriever with FAISS index and sentence transformer."""
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.index = None
        self.chunks = []
        self.web_scraper = WebScraper()
        
        # Try to load existing FAISS index
        if faiss_index_path and chunks_path:
            self._load_index(faiss_index_path, chunks_path)
        else:
            logger.warning("FAISS index path not provided. Using web sources only.")
    
    def _load_index(self, faiss_path: str, chunks_path: str) -> None:
        """Load pre-built FAISS index and chunks."""
        try:
            if os.path.exists(faiss_path) and os.path.exists(chunks_path):
                self.index = faiss.read_index(faiss_path)
                with open(chunks_path, 'rb') as f:
                    self.chunks = pickle.load(f)
                logger.info(f"Loaded FAISS index with {self.index.ntotal} vectors")
            else:
                logger.warning("FAISS index files not found")
        except Exception as e:
            logger.error(f"Error loading FAISS index: {e}")
    
    def retrieve_from_faiss(self, query: str, k: int = 5) -> list:
        """Retrieve relevant chunks from FAISS index."""
        try:
            if not self.index or not self.chunks:
                return []
            
            # Embed query
            query_embedding = self.model.encode([query], show_progress_bar=False)[0]
            query_embedding = np.array([query_embedding]).astype('float32')
            
            # Search in FAISS
            distances, indices = self.index.search(query_embedding, k)
            
            results = []
            for idx, distance in zip(indices[0], distances[0]):
                if idx < len(self.chunks):
                    results.append({
                        'source': 'knowledge_base',
                        'content': self.chunks[idx],
                        'distance': float(distance),
                        'similarity': 1 / (1 + float(distance))  # Convert distance to similarity
                    })
            
            return results
        
        except Exception as e:
            logger.error(f"Error retrieving from FAISS: {e}")
            return []
    
    def retrieve_from_web(self, query: str, topic: str = None, max_results: int = 3) -> list:
        """Retrieve relevant information from web sources."""
        try:
            if topic:
                articles = self.web_scraper.get_articles_by_topic(topic)
            else:
                # Get all cached articles and filter by query
                all_articles = self.web_scraper._get_all_cached_articles()
                
                # Simple text matching for filtering
                query_words = set(query.lower().split())
                articles = []
                
                for article in all_articles:
                    title_words = set(article.get('title', '').lower().split())
                    desc_words = set(article.get('description', '').lower().split())
                    
                    # Calculate relevance score
                    title_matches = len(query_words & title_words)
                    desc_matches = len(query_words & desc_words)
                    
                    if title_matches > 0 or desc_matches > 0:
                        articles.append({
                            'article': article,
                            'relevance': title_matches * 2 + desc_matches
                        })
                
                # Sort by relevance and take top results
                articles = sorted(articles, key=lambda x: x['relevance'], reverse=True)[:max_results]
                articles = [a['article'] for a in articles]
            
            results = []
            for article in articles[:max_results]:
                results.append({
                    'source': 'web_articles',
                    'title': article.get('title', ''),
                    'content': article.get('description', ''),
                    'article_source': article.get('source', ''),
                    'similarity': 0.85  # Default high confidence for web sources
                })
            
            return results
        
        except Exception as e:
            logger.error(f"Error retrieving from web: {e}")
            return []
    
    def hybrid_retrieve(self, query: str, k_faiss: int = 3, k_web: int = 2, use_topic: str = None) -> dict:
        """Retrieve from both FAISS and web sources."""
        try:
            faiss_results = self.retrieve_from_faiss(query, k=k_faiss)
            web_results = self.retrieve_from_web(query, topic=use_topic, max_results=k_web)
            
            # Combine and rank results
            all_results = {
                'faiss': faiss_results,
                'web': web_results,
                'combined': faiss_results + web_results,
                'total_results': len(faiss_results) + len(web_results)
            }
            
            return all_results
        
        except Exception as e:
            logger.error(f"Error in hybrid retrieval: {e}")
            return {
                'faiss': [],
                'web': [],
                'combined': [],
                'total_results': 0
            }
    
    def format_context(self, retrieved_results: dict, max_context_length: int = 2000) -> str:
        """Format retrieved results into a context string for LLM."""
        try:
            context = ""      
            # Add FAISS results
            if retrieved_results.get('faiss'):
                context += "Knowledge Base Information:\n"
                for i, result in enumerate(retrieved_results['faiss'][:2], 1):
                    context += f"{i}. {result['content'][:300]}...\n\n"
            
            # Add web results
            if retrieved_results.get('web'):
                context += "\nRecent Articles and Resources:\n"
                for i, result in enumerate(retrieved_results['web'][:2], 1):
                    context += f"{i}. {result['title']}\n"
                    context += f"   Source: {result['article_source']}\n"
                    context += f"   {result['content'][:200]}...\n\n"
            
            # Truncate if too long
            if len(context) > max_context_length:
                context = context[:max_context_length] + "..."
            
            return context
        
        except Exception as e:
            logger.error(f"Error formatting context: {e}")
            return ""
    
    def refresh_web_cache(self) -> dict:
        """Refresh cached web articles."""
        try:
            results = self.web_scraper.scrape_all_sources(max_articles_per_source=3)
            logger.info(f"Refreshed web cache with {sum(len(v) for v in results.values())} articles")
            return results
        except Exception as e:
            logger.error(f"Error refreshing web cache: {e}")
            return {}


if __name__ == "__main__":
    # Initialize retriever
    retriever = AdvancedRetriever(
        faiss_index_path='../data/faiss_index.bin',
        chunks_path='../data/chunks.pkl'
    )
    
    # Test queries
    queries = [
        "How do I manage anxiety?",
        "I'm feeling depressed",
        "Sleep problems and stress"
    ]
    
    for query in queries:
        print(f"\nQuery: {query}")
        results = retriever.hybrid_retrieve(query)
        print(f"Found {results['total_results']} results")
        print(f"Context:\n{retriever.format_context(results)}")
