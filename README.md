# Mental Health Chatbot 🧠💬

[![Open Source](https://img.shields.io/badge/Open%20Source-MIT%20License-brightgreen)](LICENSE)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Framework-Flask-red)](https://flask.palletsprojects.com/)
[![Free](https://img.shields.io/badge/Cost-FREE-success)](#-cost)

An **advanced, free, and open-source** mental health chatbot powered by data science, NLP, and vector search. Built for learning and impact.

## ✨ Features

### 🧠 Advanced Data Science
- **Semantic Search (FAISS)** - Find relevant information using meaning, not just keywords
- **Emotion Detection (Transformers)** - Understand user's emotional state in real-time
- **Text Processing (NLTK/spaCy)** - Advanced NLP preprocessing pipeline
- **Crisis Detection** - Automatic identification of concerning keywords
- **Mood Analytics** - Track trends, patterns, and wellness metrics

### 🌐 Multi-Source Knowledge
- **PDF Knowledge Base** - Your own documents indexed with FAISS
- **Real-time Web Scraping** - Latest articles from trusted sources
- **Intelligent Caching** - 24-hour cache to avoid repeated scrapes
- **Hybrid Retrieval** - Combines local + web sources automatically

### 📊 User Analytics
- **Mood Tracking** - Log daily mood (1-10 scale)
- **Trend Analysis** - Identify improving/declining/stable patterns
- **Crisis Alerts** - Automatic severity detection
- **Wellness Recommendations** - Personalized suggestions based on patterns

### 🔒 Privacy-First
- **Local Execution** - Everything runs on your machine
- **No API Keys Needed** - Completely offline capable
- **SQLite Database** - Lightweight, serverless data storage
- **No Cloud Dependency** - Full control over data

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip
- 2-3 GB disk space (for ML models)
- 4GB+ RAM recommended

### Installation (5 minutes)

```bash
# Clone repository
git clone https://github.com/Kiran-bioinfo/Chat_bot_mental_health.git
cd Chat_bot_mental_health

# Switch to advanced branch
git checkout feature/advanced-data-science

# Create virtual environment
python -m venv venv

# Activate venv
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
cd mental_health_webbot
pip install -r requirements.txt

# Run application
python app.py

# Open http://localhost:5000
```

---

## 📚 Documentation

- **[ADVANCED_SETUP_GUIDE.md](ADVANCED_SETUP_GUIDE.md)** - Complete installation & module guide
- **[advanced_mental_health_chatbot_flow.md](advanced_mental_health_chatbot_flow.md)** - Architecture deep-dive
- **[implementation_summary.md](implementation_summary.md)** - Feature overview
- **[updated_app_structure.md](updated_app_structure.md)** - Code integration guide

---

## 🏗️ Architecture

```
User Input
    ↓
[1] Data Processor
    ├─ Text cleaning & normalization
    ├─ Tokenization & lemmatization
    └─ Entity extraction
    ↓
[2] Emotion Detector
    ├─ Sentiment analysis
    ├─ Emotion classification
    ├─ Intensity scoring
    └─ Crisis detection
    ↓
[3] Hybrid Retriever
    ├─ FAISS semantic search
    ├─ Web scraping (Mindful, Psychology Today, NAMI)
    └─ Context assembly
    ↓
[4] Response Generator
    ├─ Empathetic templates
    ├─ Context integration
    └─ Crisis-safe responses
    ↓
[5] Analytics
    ├─ Mood logging
    ├─ Trend analysis
    ├─ Crisis alerts
    └─ Recommendations
    ↓
Response to User
```

---

## 📦 Core Modules

### `data_processor.py` 🔤
```python
from modules.data_processor import DataProcessor

processor = DataProcessor()
result = processor.preprocess_pipeline("I'm feeling anxious")

print(result['entities'])    # Detected: anxiety
print(result['processed'])   # Cleaned text
print(result['statistics'])  # Word count, metrics
```

**Features:**
- Text cleaning & normalization
- Lemmatization & stemming
- Mental health entity extraction
- Text statistics

### `emotion_detector.py` 😊😢
```python
from modules.emotion_detector import EmotionDetector

detector = EmotionDetector()
analysis = detector.analyze_mental_health_state("I'm very depressed")

print(analysis['emotions'])          # Detected emotions
print(analysis['intensity'])         # High/moderate/low
print(analysis['crisis_indicators']) # Crisis flags
```

**Features:**
- Sentiment analysis
- Multi-emotion classification
- Intensity scoring
- Crisis indicator detection

### `web_scraper.py` 🌐
```python
from modules.web_scraper import WebScraper

scraper = WebScraper()
articles = scraper.get_articles_by_topic('anxiety')

for article in articles:
    print(f"- {article['title']}")
```

**Features:**
- Scrapes from free sources
- Smart caching (24-hour TTL)
- Topic-based filtering
- Error handling

### `retriever.py` 🔍
```python
from modules.retriever import AdvancedRetriever

retriever = AdvancedRetriever(
    faiss_index_path='data/faiss_index.bin',
    chunks_path='data/chunks.pkl'
)

results = retriever.hybrid_retrieve("How to manage anxiety?")
context = retriever.format_context(results)
```

**Features:**
- FAISS semantic search
- Web source retrieval
- Hybrid ranking
- Context formatting

### `analytics.py` 📊
```python
from modules.analytics import MoodAnalytics

analytics = MoodAnalytics()
analytics.log_mood('user123', mood_score=7, mood_label='happy')

trends = analytics.get_mood_trends('user123', days=7)
print(f"Trend: {trends['trend']}")  # improving/declining/stable
```

**Features:**
- Mood logging & persistence
- Trend analysis
- Crisis detection
- Wellness recommendations

---

## 🎓 Data Science Techniques

| Technique | Implementation | Benefit |
|-----------|-----------------|----------|
| **Vector Embeddings** | sentence-transformers | Convert text to 384-dim vectors |
| **Semantic Search** | FAISS | Find meaning-based matches |
| **Transformers** | Hugging Face | SOTA NLP models |
| **Text Processing** | NLTK + spaCy | Robust preprocessing |
| **Classification** | HF zero-shot | Multi-emotion detection |
| **Time Series** | NumPy | Trend analysis |
| **Web Scraping** | Beautiful Soup | Real-time data |
| **Caching** | SQLite | Performance optimization |

---

## 💰 Cost

```
Total Cost: ₹0 (FREE)

Breakdown:
✓ Flask (web framework) - FREE
✓ Transformers (AI models) - FREE
✓ FAISS (vector search) - FREE
✓ SQLite (database) - FREE
✓ BeautifulSoup (scraping) - FREE
✓ NLTK + spaCy (NLP) - FREE

Total: ₹0 + Learning! 🎉
```

---

## 🗂️ Project Structure

```
Chat_bot_mental_health/
├── mental_health_webbot/
│   ├── modules/
│   │   ├── __init__.py
│   │   ├── data_processor.py         # Text preprocessing
│   │   ├── emotion_detector.py       # Emotion/sentiment
│   │   ├── web_scraper.py           # Real-time data
│   │   ├── retriever.py             # FAISS + web hybrid
│   │   └── analytics.py             # Mood tracking
│   ├── data/
│   │   ├── faiss_index.bin          # Vector index
│   │   ├── chunks.pkl               # Knowledge chunks
│   │   └── user_data.db             # SQLite database
│   ├── templates/
│   │   └── index.html               # Chat UI
│   ├── static/
│   │   ├── css/
│   │   └── js/
│   ├── app.py                       # Flask app
│   ├── config.py                    # Configuration
│   └── requirements.txt             # Dependencies
├── book_data_hackathon/             # PDF knowledge base
├── build_pdf_knowledge.py           # FAISS builder
├── ADVANCED_SETUP_GUIDE.md          # Installation guide
├── advanced_mental_health_chatbot_flow.md  # Architecture
├── implementation_summary.md         # Features
├── updated_app_structure.md         # Code guide
├── README.md                        # This file
├── LICENSE                          # MIT License
├── CONTRIBUTING.md                  # Contribution guide
├── CODE_OF_CONDUCT.md              # Community standards
└── .gitignore                       # Git ignore
```

---

## 🤝 Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### How to contribute:

1. **Fork the repository**
2. **Create feature branch** (`git checkout -b feature/your-feature`)
3. **Make changes** and test locally
4. **Commit with clear messages** (`git commit -m "Add amazing feature"`)
5. **Push to branch** (`git push origin feature/your-feature`)
6. **Open Pull Request** with description

### Areas we need help:
- 🎨 **UI/UX Improvements** - Better chat interface
- 🔧 **Bug Fixes** - Found an issue? Fix it!
- 📚 **Documentation** - Improve guides & examples
- 🧪 **Testing** - Add unit & integration tests
- 🌍 **Localization** - Translate to other languages
- 🚀 **Features** - Add new modules or capabilities

---

## 📄 License

This project is licensed under the **MIT License** - see [LICENSE](LICENSE) file for details.

You are free to:
- ✅ Use for personal/commercial projects
- ✅ Modify and distribute
- ✅ Include in your own projects
- ✅ Use in research

Just give credit! 😊

---

## 🙏 Acknowledgments

Built with:
- [Sentence Transformers](https://www.sbert.net/)
- [FAISS](https://faiss.ai/)
- [Hugging Face](https://huggingface.co/)
- [Flask](https://flask.palletsprojects.com/)
- [NLTK](https://www.nltk.org/)
- [spaCy](https://spacy.io/)
- [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/)

---

## 📧 Contact & Support

- **Issues?** Create a [GitHub Issue](https://github.com/Kiran-bioinfo/Chat_bot_mental_health/issues)
- **Discussions?** Start a [GitHub Discussion](https://github.com/Kiran-bioinfo/Chat_bot_mental_health/discussions)
- **Email:** [Your Email Here]
- **Twitter:** [@YourHandle]

---

## ⭐ Show Your Support

If this project helps you, please consider:
- ⭐ **Star the repository**
- 🔔 **Watch for updates**
- 💬 **Share feedback**
- 🤝 **Contribute**
- 📢 **Spread the word**

---

## 🚀 Roadmap

- [ ] Integrate local LLM (Ollama)
- [ ] Build mood analytics dashboard
- [ ] Multi-language support
- [ ] Mobile app (React Native)
- [ ] Voice input/output
- [ ] Advanced NER for medical conditions
- [ ] Integration with therapy resources
- [ ] Community features
- [ ] Research paper database
- [ ] Deployment templates (Docker, Heroku)

---

## ⚠️ Disclaimer

**This chatbot is NOT a substitute for professional mental health care.**

- Use for educational & support purposes only
- If experiencing crisis, contact emergency services
- Always consult qualified mental health professionals
- This tool supplements, not replaces, therapy

**Crisis Resources:**
- **India:** AASRA (9820466726), iCall (9152987821)
- **US:** National Suicide Hotline (988)
- **International:** Visit findahelpline.com

---

## 📚 Learn More

- [FAISS Documentation](https://faiss.ai/)
- [Transformers Guide](https://huggingface.co/docs/transformers/)
- [Sentence Transformers](https://www.sbert.net/)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [NLP with NLTK](https://www.nltk.org/)

---

**Built with ❤️ by [Kiran Patil](https://github.com/Kiran-bioinfo)**

*Making mental health support accessible to everyone, free and open-source.*

---

*Last updated: December 2025*
