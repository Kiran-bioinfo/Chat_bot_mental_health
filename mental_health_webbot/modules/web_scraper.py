import requests
from bs4 import BeautifulSoup
import json
import sqlite3
from datetime import datetime, timedelta
import logging
from typing import list, dict

logger = logging.getLogger(__name__)

class WebScraper:
    """Scrape mental health resources and articles from free public sources."""
    
    # Free mental health resources to scrape
    SOURCES = {
        'mindful_articles': {
            'url': 'https://www.mindful.org/basics/',
            'selector': 'article',
            'title_selector': 'h2',
            'desc_selector': 'p'
        },
        'psychology_today': {
            'url': 'https://www.psychologytoday.com/basics/anxiety',
            'selector': 'article',
            'title_selector': 'h2',
            'desc_selector': 'p'
        },
        'nami_resources': {
            'url': 'https://www.nami.org/home',
            'selector': 'div.post',
            'title_selector': 'h3',
            'desc_selector': 'p'
        }
    }
    
    def __init__(self, db_path: str = 'mental_health_webbot/data/user_data.db'):
        self.db_path = db_path
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        self.cache_ttl = 24  # Cache for 24 hours
    
    def scrape_source(self, source_name: str, max_articles: int = 5) -> list:
        """Scrape mental health articles from a specific source."""
        try:
            # Check cache first
            cached = self._get_cached_articles(source_name)
            if cached:
                logger.info(f"Using cached articles from {source_name}")
                return cached
            
            if source_name not in self.SOURCES:
                logger.error(f"Source {source_name} not found")
                return []
            
            source = self.SOURCES[source_name]
            articles = []
            
            response = self.session.get(source['url'], timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            article_elements = soup.select(source['selector'])[:max_articles]
            
            for element in article_elements:
                try:
                    title_elem = element.select_one(source['title_selector'])
                    desc_elem = element.select_one(source['desc_selector'])
                    
                    if title_elem:
                        article = {
                            'source': source_name,
                            'title': title_elem.get_text(strip=True),
                            'description': desc_elem.get_text(strip=True) if desc_elem else '',
                            'scraped_at': datetime.now().isoformat()
                        }
                        articles.append(article)
                except Exception as e:
                    logger.error(f"Error extracting article: {e}")
                    continue
            
            # Cache articles
            if articles:
                self._cache_articles(source_name, articles)
            
            return articles
        
        except Exception as e:
            logger.error(f"Error scraping {source_name}: {e}")
            return []
    
    def scrape_all_sources(self, max_articles_per_source: int = 3) -> dict:
        """Scrape articles from all configured sources."""
        all_articles = {}
        
        for source_name in self.SOURCES.keys():
            articles = self.scrape_source(source_name, max_articles_per_source)
            if articles:
                all_articles[source_name] = articles
            logger.info(f"Scraped {len(articles)} articles from {source_name}")
        
        return all_articles
    
    def get_articles_by_topic(self, topic: str) -> list:
        """Get articles related to a specific mental health topic."""
        try:
            # Map topics to search terms
            topic_mapping = {
                'anxiety': ['anxiety', 'worry', 'panic'],
                'depression': ['depression', 'sadness', 'mood'],
                'stress': ['stress', 'management', 'coping'],
                'sleep': ['sleep', 'insomnia', 'rest'],
                'relationships': ['relationships', 'connection', 'social'],
                'mindfulness': ['mindfulness', 'meditation', 'awareness']
            }
            
            search_terms = topic_mapping.get(topic.lower(), [topic.lower()])
            relevant_articles = []
            
            # Search in all cached articles
            all_cached = self._get_all_cached_articles()
            
            for article in all_cached:
                title_lower = article.get('title', '').lower()
                desc_lower = article.get('description', '').lower()
                
                if any(term in title_lower or term in desc_lower for term in search_terms):
                    relevant_articles.append(article)
            
            return relevant_articles
        
        except Exception as e:
            logger.error(f"Error getting articles by topic: {e}")
            return []
    
    def _cache_articles(self, source_name: str, articles: list) -> None:
        """Cache scraped articles in database."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Create table if not exists
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS scraped_articles (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    source TEXT,
                    title TEXT,
                    description TEXT,
                    scraped_at TIMESTAMP,
                    cached_at TIMESTAMP
                )
            ''')
            
            # Insert articles
            for article in articles:
                cursor.execute('''
                    INSERT INTO scraped_articles (source, title, description, scraped_at, cached_at)
                    VALUES (?, ?, ?, ?, ?)
                ''', (
                    article['source'],
                    article['title'],
                    article['description'],
                    article['scraped_at'],
                    datetime.now().isoformat()
                ))
            
            conn.commit()
            conn.close()
            logger.info(f"Cached {len(articles)} articles from {source_name}")
        
        except Exception as e:
            logger.error(f"Error caching articles: {e}")
    
    def _get_cached_articles(self, source_name: str) -> list:
        """Get articles cached from a specific source."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Check if cache is still valid
            cutoff_time = (datetime.now() - timedelta(hours=self.cache_ttl)).isoformat()
            
            cursor.execute('''
                SELECT source, title, description, scraped_at FROM scraped_articles
                WHERE source = ? AND cached_at > ?
                ORDER BY cached_at DESC
            ''', (source_name, cutoff_time))
            
            articles = []
            for row in cursor.fetchall():
                articles.append({
                    'source': row[0],
                    'title': row[1],
                    'description': row[2],
                    'scraped_at': row[3]
                })
            
            conn.close()
            return articles if articles else None
        
        except Exception as e:
            logger.error(f"Error retrieving cached articles: {e}")
            return None
    
    def _get_all_cached_articles(self) -> list:
        """Get all cached articles."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT source, title, description, scraped_at FROM scraped_articles
                ORDER BY cached_at DESC
            ''')
            
            articles = []
            for row in cursor.fetchall():
                articles.append({
                    'source': row[0],
                    'title': row[1],
                    'description': row[2],
                    'scraped_at': row[3]
                })
            
            conn.close()
            return articles
        
        except Exception as e:
            logger.error(f"Error retrieving all cached articles: {e}")
            return []
    
    def create_knowledge_document(self, articles: list) -> str:
        """Convert scraped articles into a knowledge document for embedding."""
        try:
            document = ""
            for article in articles:
                document += f"Title: {article.get('title', '')}\n"
                document += f"Source: {article.get('source', '')}\n"
                document += f"Content: {article.get('description', '')}\n\n"
            return document
        except Exception as e:
            logger.error(f"Error creating knowledge document: {e}")
            return ""


if __name__ == "__main__":
    scraper = WebScraper()
    
    print("Scraping mental health resources...")
    all_articles = scraper.scrape_all_sources(max_articles_per_source=2)
    
    for source, articles in all_articles.items():
        print(f"\n{source}: {len(articles)} articles")
        for article in articles:
            print(f"  - {article['title']}")
    
    print("\nSearching for articles on 'anxiety'...")
    anxiety_articles = scraper.get_articles_by_topic('anxiety')
    print(f"Found {len(anxiety_articles)} articles")
