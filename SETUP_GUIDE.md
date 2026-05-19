# 🎯 Student Setup Guide

## 📋 Complete Setup Checklist

Follow this step-by-step guide to get your Mental Health Chatbot running locally.

### ✅ Step 1: System Requirements Check

**Before you start, make sure you have:**
- [ ] Python 3.8 or higher installed
- [ ] Git installed
- [ ] A code editor (VS Code, PyCharm, etc.)
- [ ] Terminal/Command Prompt access

**Check your Python version:**
```bash
python3 --version
# Should show Python 3.8.x or higher
```

**Check if pip is available:**
```bash
pip3 --version
# Should show pip version information
```

### ✅ Step 2: Download the Project

**Option A: Clone from GitHub (if available)**
```bash
git clone <repository-url>
cd mental_health_chatbot
```

**Option B: Download ZIP file**
1. Download the project ZIP file
2. Extract to a folder called `mental_health_chatbot`
3. Open terminal in that folder

### ✅ Step 3: Set Up Virtual Environment

**Why use a virtual environment?**
- Keeps project dependencies separate
- Prevents conflicts with other Python projects
- Makes deployment easier

**Create and activate virtual environment:**
```bash
# Create virtual environment
python3 -m venv venv

# Activate it (choose your operating system):

# On macOS/Linux:
source venv/bin/activate

# On Windows (Command Prompt):
venv\Scripts\activate

# On Windows (PowerShell):
venv\Scripts\Activate.ps1
```

**You'll know it's active when you see `(venv)` in your terminal prompt.**

### ✅ Step 4: Install Dependencies

```bash
# Make sure virtual environment is active (you should see (venv) in prompt)
pip install -r requirements.txt
```

**This will install:**
- Streamlit (web interface)
- NLTK (natural language processing)
- Pandas (data handling)
- Matplotlib (charts)
- Scikit-learn (machine learning)

### ✅ Step 5: Run the Application

```bash
streamlit run app.py
```

**What should happen:**
1. Terminal shows "You can now view your Streamlit app in your browser"
2. Browser automatically opens to http://localhost:8501
3. You see the chatbot interface

### ✅ Step 6: Test the Chatbot

**Try these test messages:**
1. "Hello" (should get a greeting)
2. "I'm stressed about exams" (should get exam-specific advice)
3. "I feel anxious" (should get anxiety coping strategies)
4. Check the mood tracking chart in the sidebar

## 🚨 Common Setup Problems & Solutions

### Problem: "python3: command not found"
**Solution:** Install Python from [python.org](https://python.org)

### Problem: "pip3: command not found"
**Solution:** 
```bash
# On macOS with Homebrew:
brew install python3

# On Ubuntu/Debian:
sudo apt-get install python3-pip

# On Windows: Reinstall Python with "Add to PATH" checked
```

### Problem: "externally-managed-environment"
**Solution:** Always use virtual environment (Step 3)

### Problem: Streamlit won't start
**Solution:**
```bash
# Kill any existing processes
pkill -f streamlit

# Try with headless mode
streamlit run app.py --server.headless true

# Or try a different port
streamlit run app.py --server.port 8502
```

### Problem: "ModuleNotFoundError"
**Solution:**
```bash
# Make sure virtual environment is active
source venv/bin/activate  # or appropriate command for your OS

# Reinstall requirements
pip install -r requirements.txt
```

## 📁 Project Structure

```
mental_health_chatbot/
├── app.py                 # Main chatbot application
├── requirements.txt       # Python dependencies
├── README.md             # Project documentation
├── SETUP_GUIDE.md        # This file
├── TROUBLESHOOTING.md    # Problem-solving guide
├── DEPLOYMENT.md         # Deployment instructions
├── venv/                 # Virtual environment (after setup)
└── chatbot.db           # Database (created automatically)
```

## 🎨 Customizing Your Chatbot

### Adding New Coping Strategies
Edit `app.py` and find the `SPECIFIC_REMEDIES` dictionary:
```python
SPECIFIC_REMEDIES = {
    'exam_anxiety': [
        "Your new study tip here...",
        # Add more strategies
    ]
}
```

### Modifying Crisis Keywords
Find the `CRISIS_KEYWORDS` list in `app.py`:
```python
CRISIS_KEYWORDS = [
    "suicide", "kill myself", 
    # Add more keywords to detect
]
```

### Changing the Interface
Modify the Streamlit UI sections in `app.py`:
- Look for `st.title()`, `st.markdown()`, etc.
- Change colors, text, layout as needed

## 🔄 Development Workflow

### Daily Development:
1. **Activate environment:** `source venv/bin/activate`
2. **Make changes** to `app.py`
3. **Test changes:** Streamlit auto-reloads when you save
4. **Commit changes:** `git add . && git commit -m "Description"`

### Adding New Features:
1. **Plan the feature** (what problem does it solve?)
2. **Code the feature** in appropriate sections
3. **Test thoroughly** with different inputs
4. **Update documentation** if needed

## 📊 Understanding the Code

### Key Components:

1. **Sentiment Analysis** (`get_sentiment()`)
   - Uses NLTK's VADER analyzer
   - Returns score from -1 (negative) to +1 (positive)

2. **Emotion Detection** (`detect_emotion_keywords()`)
   - Looks for specific emotion words
   - Returns list of detected emotions

3. **Response Generation** (`get_contextual_response()`)
   - Main logic for chatbot responses
   - Considers conversation history and context

4. **Database Operations** (`save_interaction()`, `get_mood_history()`)
   - Stores conversations in SQLite
   - Retrieves data for mood tracking

### Data Flow:
```
User Input → Emotion Detection → Sentiment Analysis → 
Context Analysis → Response Generation → Database Storage → 
UI Update
```

## 🎓 Learning Opportunities

### Extend Your Project:
1. **Add new emotions** to detect and respond to
2. **Implement user profiles** for personalized responses
3. **Add voice input/output** using speech APIs
4. **Create a mobile app** version
5. **Integrate with calendar** for mood tracking over time

### Technical Skills You'll Learn:
- Natural Language Processing (NLP)
- Sentiment Analysis
- Database Management
- Web Development with Streamlit
- Python Programming
- Git Version Control
- Deployment and DevOps

## 🤝 Getting Help

### If you're stuck:
1. **Check the error message** carefully
2. **Read the TROUBLESHOOTING.md** file
3. **Search online** for the specific error
4. **Ask for help** with detailed error information

### Resources:
- [Streamlit Documentation](https://docs.streamlit.io)
- [NLTK Documentation](https://www.nltk.org)
- [Python Documentation](https://docs.python.org)
- [Stack Overflow](https://stackoverflow.com) for coding questions

---

**🎉 Congratulations!** You now have a working mental health chatbot. Remember, this is a learning project - experiment, break things, and learn from the process!
