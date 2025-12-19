import re
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import logging

# Ensure NLTK data is available
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')
    nltk.download('stopwords')
    nltk.download('wordnet')

logger = logging.getLogger(__name__)

class DataProcessor:
    """Advanced text preprocessing and data processing."""
    
    def __init__(self):
        self.lemmatizer = WordNetLemmatizer()
        self.stop_words = set(stopwords.words('english'))
        self.mental_health_terms = self._load_mental_health_terms()
    
    def _load_mental_health_terms(self):
        """Load mental health specific terminology."""
        return {
            'anxiety': ['anxious', 'worried', 'nervous', 'panic'],
            'depression': ['sad', 'depressed', 'hopeless', 'worthless'],
            'stress': ['stressed', 'overwhelmed', 'pressure', 'tense'],
            'insomnia': ['can\'t sleep', 'sleepless', 'insomnia', 'restless'],
            'loneliness': ['alone', 'isolated', 'lonely', 'disconnected'],
        }
    
    def clean_text(self, text: str) -> str:
        """Clean text by removing special characters and extra whitespace."""
        # Convert to lowercase
        text = text.lower()
        
        # Remove URLs
        text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
        
        # Remove email addresses
        text = re.sub(r'\S+@\S+', '', text)
        
        # Remove special characters but keep punctuation for sentence boundary
        text = re.sub(r'[^a-zA-Z0-9\s\.!?\-]', '', text)
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text
    
    def tokenize_sentences(self, text: str) -> list:
        """Tokenize text into sentences."""
        try:
            sentences = sent_tokenize(text)
            return [s.strip() for s in sentences if len(s.strip()) > 0]
        except Exception as e:
            logger.error(f"Error tokenizing sentences: {e}")
            return text.split('.')
    
    def tokenize_words(self, text: str) -> list:
        """Tokenize text into words."""
        try:
            words = word_tokenize(text)
            return [w for w in words if w.isalpha()]
        except Exception as e:
            logger.error(f"Error tokenizing words: {e}")
            return text.split()
    
    def lemmatize(self, text: str) -> str:
        """Apply lemmatization to text."""
        try:
            words = word_tokenize(text)
            lemmatized = [self.lemmatizer.lemmatize(w) for w in words]
            return ' '.join(lemmatized)
        except Exception as e:
            logger.error(f"Error lemmatizing: {e}")
            return text
    
    def remove_stopwords(self, text: str) -> str:
        """Remove common English stopwords."""
        words = text.split()
        filtered = [w for w in words if w.lower() not in self.stop_words]
        return ' '.join(filtered)
    
    def extract_entities(self, text: str) -> dict:
        """Extract mental health entities from text."""
        entities = {
            'mental_health_terms': [],
            'emotions': [],
            'intensity_words': []
        }
        
        # Check for mental health terms
        for category, terms in self.mental_health_terms.items():
            for term in terms:
                if term in text.lower():
                    entities['mental_health_terms'].append(category)
        
        # Extract intensity words
        intensity_words = ['very', 'extremely', 'really', 'absolutely', 'severely', 'mildly', 'slightly']
        for word in intensity_words:
            if word in text.lower():
                entities['intensity_words'].append(word)
        
        # Remove duplicates
        entities['mental_health_terms'] = list(set(entities['mental_health_terms']))
        entities['intensity_words'] = list(set(entities['intensity_words']))
        
        return entities
    
    def get_text_statistics(self, text: str) -> dict:
        """Get statistical information about the text."""
        sentences = self.tokenize_sentences(text)
        words = self.tokenize_words(text)
        
        return {
            'word_count': len(words),
            'sentence_count': len(sentences),
            'avg_words_per_sentence': len(words) / max(len(sentences), 1),
            'unique_words': len(set(words)),
            'text_length': len(text)
        }
    
    def preprocess_pipeline(self, text: str, remove_stop_words: bool = True) -> dict:
        """Complete preprocessing pipeline."""
        try:
            # Step 1: Clean
            cleaned = self.clean_text(text)
            
            # Step 2: Extract entities early (before lemmatization)
            entities = self.extract_entities(cleaned)
            
            # Step 3: Lemmatize
            lemmatized = self.lemmatize(cleaned)
            
            # Step 4: Remove stopwords (optional)
            if remove_stop_words:
                processed = self.remove_stopwords(lemmatized)
            else:
                processed = lemmatized
            
            # Step 5: Get statistics
            stats = self.get_text_statistics(original_text=text)
            
            return {
                'original': text,
                'cleaned': cleaned,
                'processed': processed,
                'sentences': self.tokenize_sentences(cleaned),
                'entities': entities,
                'statistics': stats
            }
        except Exception as e:
            logger.error(f"Error in preprocessing pipeline: {e}")
            return {
                'original': text,
                'cleaned': text,
                'processed': text,
                'sentences': [text],
                'entities': {},
                'statistics': {}
            }


if __name__ == "__main__":
    processor = DataProcessor()
    test_text = "I'm feeling very anxious and can't sleep. This stress is overwhelming me."
    
    result = processor.preprocess_pipeline(test_text)
    print("Original:", result['original'])
    print("Cleaned:", result['cleaned'])
    print("Processed:", result['processed'])
    print("Entities:", result['entities'])
    print("Statistics:", result['statistics'])
