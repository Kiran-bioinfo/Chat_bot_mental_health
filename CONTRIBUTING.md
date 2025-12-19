# Contributing to Mental Health Chatbot 🤝

Thank you for your interest in contributing! This document provides guidelines and instructions for contributing to this project.

## Code of Conduct

We are committed to providing a welcoming and inclusive environment for all contributors.

### Our Values
- 🤝 **Be Respectful** - Treat all contributors with respect
- 💡 **Be Inclusive** - Welcome diverse perspectives and experiences
- 🔍 **Be Constructive** - Give helpful feedback and advice
- 🙏 **Be Patient** - Help is given voluntarily

---

## Getting Started

### 1. Fork the Repository

```bash
# Click "Fork" on GitHub
# Then clone your fork
git clone https://github.com/YOUR-USERNAME/Chat_bot_mental_health.git
cd Chat_bot_mental_health
```

### 2. Create a Feature Branch

```bash
# Always branch from latest feature/advanced-data-science
git fetch origin feature/advanced-data-science
git checkout feature/advanced-data-science
git checkout -b feature/your-feature-name
```

### 3. Set Up Development Environment

```bash
# Create virtual environment
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
cd mental_health_webbot
pip install -r requirements.txt

# Install dev dependencies
pip install pytest pytest-cov black flake8
```

### 4. Make Your Changes

```bash
# Edit files
# Test locally
# Commit regularly
```

---

## Types of Contributions

### 🐛 Bug Reports

**Found a bug?** Please report it!

1. **Check existing issues** - Don't duplicate
2. **Provide details:**
   - Python version
   - Operating system
   - Steps to reproduce
   - Expected vs actual behavior
   - Error messages/logs
3. **Include code snippets** if possible

**Example:**
```
Title: Emotion detector crashes with empty string

Environment:
- Python 3.9
- Windows 10

Steps:
1. Call detector.analyze_mental_health_state("")
2. Get KeyError

Expected: Handle empty gracefully
Actual: Crashes
```

### ✨ Feature Requests

**Have an idea?** We'd love to hear it!

1. **Describe the feature** - What problem does it solve?
2. **Provide examples** - How would users interact?
3. **List alternatives** - Other approaches considered?
4. **Explain impact** - Who benefits?

**Example:**
```
Feature: Multi-language support

Problem: Many non-English speakers can't use the chatbot

Proposal: Use Google Translate API + locale detection

Example:
- User writes in Spanish
- Auto-detect language
- Translate to English internally
- Response translated back

Benefit: Accessible to millions more users
```

### 📝 Documentation

**Improve our docs!**

- Fix typos
- Clarify confusing sections
- Add examples
- Improve formatting
- Add diagrams

### 🧪 Tests

**Write tests!**

```python
# tests/test_emotion_detector.py
import pytest
from modules.emotion_detector import EmotionDetector

def test_detect_crisis():
    detector = EmotionDetector()
    result = detector.detect_crisis("I want to kill myself")
    assert result['is_crisis'] == True
    assert result['severity_score'] > 0.7

def test_neutral_text():
    detector = EmotionDetector()
    result = detector.detect_crisis("The weather is nice today")
    assert result['is_crisis'] == False
```

### 🎨 UI/UX Improvements

- Improve chat interface
- Better mobile experience
- Accessibility improvements
- New visualizations

### 🔧 Code Improvements

- Refactor inefficient code
- Add error handling
- Improve performance
- Better logging
- Code organization

---

## Development Workflow

### 1. Code Style

We follow PEP 8 with Black formatter:

```bash
# Format your code
black mental_health_webbot/

# Check style
flake8 mental_health_webbot/
```

### 2. Commit Messages

Write clear, descriptive commit messages:

```
good:
  "Fix: Prevent crash when emotion_detector receives empty string"
  "Feature: Add multi-language support for Spanish"
  "Docs: Update FAISS configuration in setup guide"
  "Test: Add unit tests for analytics module"

bad:
  "fix stuff"
  "update"
  "bug"
  "asdf"
```

**Format:**
```
<type>: <subject>

<body (optional)>

<footer (optional)>
```

**Types:**
- `Feature:` New functionality
- `Fix:` Bug fix
- `Docs:` Documentation change
- `Test:` Test addition/modification
- `Refactor:` Code structure (no functional change)
- `Perf:` Performance improvement
- `Style:` Formatting (not affecting code logic)

### 3. Testing

Before submitting, test locally:

```bash
# Run all tests
pytest

# Run specific test
pytest tests/test_emotion_detector.py

# Run with coverage
pytest --cov=mental_health_webbot
```

### 4. Testing Modules Individually

```bash
# Test data processor
python -m modules.data_processor

# Test emotion detector
python -m modules.emotion_detector

# Test web scraper
python -m modules.web_scraper

# Test analytics
python -m modules.analytics
```

---

## Pull Request Process

### Before Submitting

- [ ] Tests pass locally
- [ ] Code follows PEP 8 (black formatted)
- [ ] No merge conflicts
- [ ] Updated documentation if needed
- [ ] Added tests for new features
- [ ] Commit messages are clear

### Submit Pull Request

1. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

2. **Open PR on GitHub**
   - Click "New Pull Request"
   - Set base to `feature/advanced-data-science`
   - Describe changes clearly

3. **PR Description Template**
   ```
   ## Description
   Brief description of changes

   ## Type of Change
   - [ ] Bug fix
   - [ ] New feature
   - [ ] Documentation update

   ## Related Issues
   Closes #123

   ## How to Test
   Steps to verify the changes work

   ## Screenshots (if applicable)
   Add screenshots for UI changes
   ```

### Review Process

- We'll review your PR within 7 days
- May request changes
- Once approved, we'll merge to `feature/advanced-data-science`
- After testing, merge to `main`
- You're officially a contributor! 🎉

---

## Areas We Need Help

### High Priority 🔴
- [ ] LLM integration (Ollama)
- [ ] Mobile app (React Native)
- [ ] Production deployment (Docker, Kubernetes)
- [ ] Database optimization

### Medium Priority 🟡
- [ ] UI/UX improvements
- [ ] More comprehensive tests
- [ ] Multi-language support
- [ ] Analytics dashboard

### Low Priority 🟢
- [ ] Code refactoring
- [ ] Documentation
- [ ] Minor bug fixes
- [ ] Performance optimization

---

## Development Tips

### Debugging

```python
# Add logging
import logging
logger = logging.getLogger(__name__)
logger.debug(f"Variable: {variable}")

# Use pdb for interactive debugging
import pdb; pdb.set_trace()
```

### Performance Profiling

```bash
# Profile your code
python -m cProfile -s cumulative app.py
```

### Memory Optimization

```python
# Check memory usage
import tracemalloc
tracemalloc.start()
# Your code here
current, peak = tracemalloc.get_traced_memory()
print(f"Memory: {current / 1024 / 1024:.1f} MB")
```

---

## Project Structure

When adding new features, maintain structure:

```
mental_health_webbot/
├── modules/              # Core functionality
│   ├── new_module.py     # Your new feature
│   └── __init__.py
├── data/                 # Data files
├── templates/            # HTML templates
├── static/               # CSS, JS, images
└── app.py               # Main Flask app

tests/                    # Unit tests
├── test_new_module.py    # Tests for your feature
```

---

## Documentation Standards

### Function Documentation

```python
def analyze_mood(text: str) -> dict:
    """Analyze mood from text input.
    
    Args:
        text: User input string to analyze
        
    Returns:
        Dictionary containing:
        - mood_score (int): 1-10 mood rating
        - emotion (str): Detected emotion
        - confidence (float): Confidence score
        
    Raises:
        ValueError: If text is empty
        
    Example:
        >>> result = analyze_mood("I'm happy")
        >>> print(result['mood_score'])
        8
    """
    pass
```

---

## Community

### Get Help
- **Questions?** Open a Discussion
- **Bug?** Open an Issue
- **Ideas?** Start a Discussion
- **Chat?** Join our Discord (coming soon)

### Code Review
- We value constructive feedback
- All reviews are respectful and helpful
- Reviewers are volunteers - be patient

---

## Recognition

All contributors are recognized:
- Listed in README.md
- Credit in commit messages
- Thank you comments in PRs
- Featured in release notes

---

## Questions?

Refer to:
1. Existing issues/discussions
2. Documentation in repo
3. Open an issue with `[QUESTION]` tag

---

## Final Notes

- Start small - even tiny fixes help!
- Don't be intimidated - we're all learning
- Ask questions - we're here to help
- Have fun - this is a community effort

**Thank you for making this project better! ❤️**

---

*Last updated: December 2025*
