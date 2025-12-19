# Advanced Mental Health Chatbot - Complete Setup Guide

## 🎯 Overview

This guide will help you set up the advanced data science version of the mental health chatbot with:
- **Semantic Search** (FAISS vector database)
- **Emotion Detection** (Transformer models)
- **Web Scraping** (Real-time data)
- **Mood Analytics** (Trend analysis & crisis detection)
- **Data Processing** (NLP preprocessing)

**Total Setup Time:** 20-30 minutes  
**Cost:** ₹0 (Completely FREE)

---

## 📋 Prerequisites

- Python 3.8+ installed
- pip (Python package manager)
- Git installed
- ~2-3 GB disk space (for ML models)
- 4GB+ RAM recommended

### Check Prerequisites
```bash
python --version          # Should be 3.8+
pip --version            # Should exist
git --version            # Should exist
```

---

## 🚀 Installation Steps

### Step 1: Clone/Update Repository

```bash
# Navigate to your project
cd Chat_bot_mental_health

# Fetch the advanced feature branch
git fetch origin feature/advanced-data-science

# Switch to advanced branch
git checkout feature/advanced-data-science
```

### Step 2: Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate it
# On Windows:
venv\Scripts\activate

# On Mac/Linux:
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
cd mental_health_webbot

# Install all requirements
pip install -r requirements.txt

# This will install:
# - Flask (web framework)
# - Transformers (emotion detection)
# - FAISS (vector search)
# - Beautiful Soup (web scraping)
# - NLTK & spaCy (text processing)
# - And more...

# Installation time: 5-10 minutes (first time)
```

### Step 4: Download NLTK Data

```bash
python -m nltk.downloader punkt stopwords wordnet averaged_perceptron_tagger
```

### Step 5: Setup Database

```bash
# Run setup script to initialize SQLite database
python setup_database.py

# This creates:
# - user_data.db (SQLite database)
# - Tables for mood logs, conversations, crisis alerts
```

### Step 6: Prepare FAISS Index (Optional but Recommended)

If you have PDFs in `book_data_hackathon/`:

```bash
# Go back to root directory
cd ..

# Build knowledge base from PDFs
python build_pdf_knowledge.py

# This generates:
# - faiss_index.bin (vector index)
# - chunks.pkl (knowledge chunks)
```

If you don't have PDFs yet, you can skip this - the web scraper will handle it!

---

## 🏃 Quick Start

### Start the Application

```bash
cd mental_health_webbot

# Run Flask app
python app.py

# You should see:
# * Running on http://localhost:5000
```

### Open in Browser

Go to: `http://localhost:5000`

---

## 📊 Data Flow Explained

### When User Sends Message:

```
1. User Input
   ↓
2. Data Preprocessing (data_processor.py)
   - Clean text
   - Tokenize
   - Extract entities
   ↓
3. Emotion Detection (emotion_detector.py)
   - Sentiment analysis
   - Emotion classification
   - Intensity scoring
   ↓
4. Hybrid Retrieval (retriever.py)
   - FAISS search (your knowledge base)
   - Web scraping (real-time articles)
   - Context assembly
   ↓
5. Crisis Detection (analytics.py)
   - Check for crisis keywords
   - Calculate severity
   - Log if needed
   ↓
6. Response Generation
   - Combine all context
   - Generate empathetic response
   ↓
7. Analytics Logging (analytics.py)
   - Log conversation
   - Update mood trends
   - Store analytics
   ↓
8. Send Response to User
```

---

## 🔧 Module Overview

### `data_processor.py`
**Purpose:** Advanced text preprocessing

```python
from modules.data_processor import DataProcessor

processor = DataProcessor()
result = processor.preprocess_pipeline("I'm feeling anxious")

print(result['entities'])     # {'mental_health_terms': ['anxiety']}
print(result['processed'])    # Cleaned, lemmatized text
print(result['statistics'])   # Word count, sentence metrics
```

**Features:**
- Text cleaning & normalization
- Lemmatization
- Stopword removal
- Entity extraction
- Mental health term detection
- Text statistics

---

### `emotion_detector.py`
**Purpose:** Detect emotions and sentiment from text

```python
from modules.emotion_detector import EmotionDetector

detector = EmotionDetector()
analysis = detector.analyze_mental_health_state("I'm extremely depressed")

print(analysis['emotions'])           # Top emotions detected
print(analysis['intensity'])          # Intensity level (0-1)
print(analysis['crisis_indicators'])  # Boolean for crisis detection
```

**Features:**
- Sentiment analysis (positive/negative)
- Multi-emotion classification
- Emotional intensity scoring
- Crisis indicator detection
- Mental health state classification

---

### `web_scraper.py`
**Purpose:** Collect real-time mental health data from web

```python
from modules.web_scraper import WebScraper

scraper = WebScraper()

# Scrape specific source
articles = scraper.scrape_source('mindful_articles', max_articles=5)

# Scrape all sources
all_articles = scraper.scrape_all_sources()

# Get articles by topic
anxiety_articles = scraper.get_articles_by_topic('anxiety')
```

**Features:**
- Scrape from multiple free sources
- Automatic caching (avoid repeated scrapes)
- Topic-based filtering
- Error handling
- 24-hour TTL for cached data

**Configured Sources:**
- Mindful.org (meditation & mindfulness)
- Psychology Today (psychology articles)
- NAMI (national alliance resources)

---

### `retriever.py`
**Purpose:** Hybrid retrieval (FAISS + Web)

```python
from modules.retriever import AdvancedRetriever

retriever = AdvancedRetriever(
    faiss_index_path='data/faiss_index.bin',
    chunks_path='data/chunks.pkl'
)

# Hybrid search
results = retriever.hybrid_retrieve(
    query="How to manage anxiety?",
    k_faiss=3,      # Top 3 from knowledge base
    k_web=2         # Top 2 from web
)

# Format for LLM
context = retriever.format_context(results)
print(context)  # Ready to use as LLM context
```

**Features:**
- Semantic search with FAISS
- Web source retrieval
- Combined ranking
- Context formatting
- Dynamic source balancing

---

### `analytics.py`
**Purpose:** Mood tracking and analytics

```python
from modules.analytics import MoodAnalytics

analytics = MoodAnalytics()

# Log mood
analytics.log_mood(
    user_id='user123',
    mood_score=7,
    mood_label='happy',
    emotions=['joy', 'contentment'],
    triggers=['exercise']
)

# Get trends
trends = analytics.get_mood_trends('user123', days=7)
print(trends['average_mood'])     # 7.2
print(trends['trend'])            # 'improving' / 'declining' / 'stable'

# Detect crisis
crisis = analytics.detect_crisis("I want to end it all")
if crisis['is_crisis']:
    analytics.log_crisis_alert('user123', crisis['crisis_types'][0], 
                              crisis['severity_score'], user_message)

# Get recommendations
recs = analytics.get_wellness_recommendations('user123')
for rec in recs:
    print(f"- {rec}")
```

**Features:**
- Mood logging and persistence
- Trend analysis (improving/declining/stable)
- Crisis detection & severity scoring
- Wellness recommendations
- Conversation logging
- Statistical analysis (numpy)

---

## 📈 Data Science Techniques Used

| Technique | Module | Purpose |
|-----------|--------|----------|
| **Vector Embeddings** | retriever.py | Convert text to vectors for similarity search |
| **Semantic Search** | retriever.py | Find contextually relevant information |
| **Transformer Models** | emotion_detector.py | State-of-the-art NLP tasks |
| **Text Processing** | data_processor.py | Clean & normalize user input |
| **Classification** | emotion_detector.py, analytics.py | Categorize emotions & detect crisis |
| **Trend Analysis** | analytics.py | Identify patterns in mood data |
| **Caching Strategy** | web_scraper.py | Optimize performance |
| **Web Scraping** | web_scraper.py | Collect external data |
| **Statistical Analysis** | analytics.py | Calculate averages, trends, patterns |

---

## 🔄 Testing Modules

### Test Data Processor
```bash
cd mental_health_webbot
python -m modules.data_processor
```

### Test Emotion Detector
```bash
python -m modules.emotion_detector
```

### Test Web Scraper
```bash
python -m modules.web_scraper
```

### Test Analytics
```bash
python -m modules.analytics
```

---

## 📝 Environment Configuration

Create `.env` file in `mental_health_webbot/`:

```env
# Flask Config
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=your-secret-key-here

# Database
DATABASE_PATH=data/user_data.db
FAISS_INDEX_PATH=data/faiss_index.bin
CHUNKS_PATH=data/chunks.pkl

# Scraping Config
WEB_SCRAPER_CACHE_TTL=24  # hours
MAX_ARTICLES_PER_SOURCE=5

# Model Config
EMBEDDING_MODEL=all-MiniLM-L6-v2
MINIMUM_SIMILARITY=0.3
```

---

## 🚨 Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'transformers'"
**Solution:**
```bash
pip install --upgrade transformers torch
```

### Issue: "FAISS not found"
**Solution:**
```bash
pip install faiss-cpu
# If on GPU: pip install faiss-gpu
```

### Issue: "NLTK data not found"
**Solution:**
```bash
python -m nltk.downloader punkt stopwords wordnet
```

### Issue: "Connection timeout during web scraping"
**Solution:**
- Check internet connection
- Web scraper has 10-second timeout
- Cached data will be used if scraping fails

### Issue: "Database is locked"
**Solution:**
- Close any other instances of the app
- Delete `user_data.db` and restart

---

## 📊 Performance Optimization Tips

### 1. Use GPU for Transformers (if available)
```bash
# Install GPU support
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
pip install faiss-gpu
```

### 2. Add Redis Caching (Optional)
```bash
pip install redis
# Cache web scraping results for 24 hours
```

### 3. Batch Processing
```python
# Process multiple texts at once
emotions = detector.detect_emotions(batch_texts)
```

### 4. Index Optimization
```python
# Use GPUIndex for faster search
import faiss
index = faiss.IndexFlatL2(dimension)
# Convert to GPU if available
```

---

## 📚 Next Steps

### Beginner
1. ✅ Install all modules
2. ✅ Test individual modules
3. ✅ Run basic chatbot
4. Add UI improvements

### Intermediate
1. Integrate Ollama for local LLM
2. Add conversation memory
3. Build mood dashboard
4. Deploy to cloud (Heroku, Railway)

### Advanced
1. Fine-tune emotion detection models
2. Add multi-language support
3. Implement vector database (Pinecone/Weaviate)
4. Add recommendation engine
5. Research paper integration

---

## 🎓 Learning Resources

- [FAISS Documentation](https://faiss.ai/)
- [Hugging Face Transformers](https://huggingface.co/docs/transformers/)
- [spaCy NLP](https://spacy.io/)
- [Sentence Transformers](https://www.sbert.net/)
- [Beautiful Soup Guide](https://www.crummy.com/software/BeautifulSoup/)

---

## 🤝 Support

If you face issues:
1. Check console logs for error messages
2. Read error message carefully
3. Check this troubleshooting section
4. Create GitHub issue with error details

---

## ✨ Features Summary

✅ Advanced text preprocessing  
✅ Emotion & sentiment detection  
✅ Semantic similarity search (FAISS)  
✅ Real-time web scraping  
✅ Mood trend analysis  
✅ Crisis detection & alerts  
✅ Conversation logging  
✅ Wellness recommendations  
✅ 100% free & open-source  
✅ Privacy-focused (runs locally)  

---

**Happy coding! 🚀**
