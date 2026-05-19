# 💬 Mental Health Support Chatbot for Students

> An empathetic, AI-powered chatbot designed to provide mental health support, mood tracking, and coping strategies for students dealing with stress, anxiety, and other challenges.

## 🌟 Features

### 🧠 **Intelligent Conversation**
- **Context-aware responses** that build on previous conversations
- **Emotion detection** for stress, anxiety, sadness, anger, and loneliness
- **Crisis detection** with immediate resource referrals
- **Solution-focused approach** providing actionable coping strategies

### 📊 **Mood Tracking & Analytics**
- Real-time sentiment analysis of conversations
- Visual mood trend charts and insights
- Session statistics and conversation history
- SQLite database for secure local storage

### 🎯 **Targeted Support**
- **Exam Anxiety**: Study strategies, test-taking tips, thought reframing
- **Work Stress**: Task prioritization, time management, communication
- **Relationship Issues**: Communication techniques, boundary setting
- **Family Stress**: Safe spaces, healthy distance, support seeking
- **General Anxiety**: Mindfulness, lifestyle changes, sleep hygiene
- **Depression Support**: Light exposure, small goals, professional help

### 🆘 **Crisis Support**
- Automatic detection of crisis keywords
- Immediate access to crisis hotlines and resources
- Professional mental health resource referrals

## 🛠️ Technology Stack

- **Frontend**: Streamlit (Interactive web interface)
- **Backend**: Python 3.8+
- **NLP**: NLTK with VADER sentiment analysis
- **Database**: SQLite (local storage)
- **Visualization**: Matplotlib, Pandas
- **Deployment**: Streamlit Cloud, Heroku, or local hosting

## 🚀 Quick Start Guide

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Git (for cloning the repository)

### 1. Clone the Repository
```bash
git clone <your-repository-url>
cd mental_health_chatbot
```

### 2. Set Up Virtual Environment (Recommended)
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Application
```bash
streamlit run app.py
```

### 5. Access the Chatbot
Open your web browser and navigate to:
- **Local URL**: http://localhost:8501
- The chatbot interface will load automatically

## 📱 How to Use

1. **Start Chatting**: Type your feelings or concerns in the input box
2. **Get Support**: Receive empathetic responses and practical coping strategies
3. **Track Mood**: View your mood trends in the sidebar dashboard
4. **Access Resources**: Use quick access buttons for crisis support and coping strategies
5. **Monitor Progress**: Check session statistics and conversation history

### Example Conversations
```
You: "I'm really stressed about my upcoming exams"
Bot: "Exam anxiety is really common and completely understandable. Here are some strategies that can help:

📚 Study Strategy: Break your study material into small, manageable chunks. Study for 25 minutes, then take a 5-minute break (Pomodoro Technique).

Would you like more study strategies or relaxation techniques?"
```

## 🔧 Configuration

### Database Setup
The chatbot automatically creates a SQLite database (`chatbot.db`) on first run. No additional configuration needed.

### Customizing Responses
You can modify response templates in `app.py`:
- `EMPATHY_RESPONSES`: Empathetic response templates
- `SPECIFIC_REMEDIES`: Targeted coping strategies
- `CRISIS_KEYWORDS`: Keywords that trigger crisis responses

## 🚀 Deployment Options

### Option 1: Streamlit Cloud (Recommended for Students)
1. Push your code to GitHub
2. Connect your GitHub repo to [Streamlit Cloud](https://streamlit.io/cloud)
3. Deploy with one click - it's free!

### Option 2: Heroku
1. Create a `Procfile` with: `web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0`
2. Deploy to Heroku following their Python app guide

### Option 3: Local Network Sharing
```bash
streamlit run app.py --server.address=0.0.0.0
```
Access from other devices on your network using your computer's IP address.

## 🛡️ Privacy & Security

- **Local Storage**: All conversations are stored locally in SQLite
- **No External APIs**: Sentiment analysis runs locally using NLTK
- **Privacy First**: No data is sent to external servers (unless deployed)
- **Anonymous Usage**: No personal identification required

## 🆘 Crisis Resources

**Immediate Help:**
- **Crisis Text Line**: Text HOME to 741741
- **National Suicide Prevention Lifeline**: 988
- **Emergency Services**: 911

**Mental Health Resources:**
- [National Alliance on Mental Illness (NAMI)](https://nami.org)
- [Mental Health America](https://mhanational.org)
- [Crisis Text Line](https://crisistextline.org)

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. **Report Issues**: Found a bug? Report it in the issues section
2. **Suggest Features**: Have ideas for new coping strategies or features?
3. **Improve Responses**: Help make the chatbot more empathetic and helpful
4. **Add Resources**: Contribute mental health resources and crisis information

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Important Disclaimers

- **Not a Replacement for Professional Help**: This chatbot is a supportive tool, not a substitute for professional mental health treatment
- **Crisis Situations**: If you're in immediate danger, please contact emergency services (911) or a crisis hotline
- **Persistent Symptoms**: If you're experiencing persistent mental health symptoms, please consult with a mental health professional

## 📞 Support

If you need help with the technical setup:
1. Check the [Troubleshooting Guide](TROUBLESHOOTING.md)
2. Review common issues in the FAQ section
3. Create an issue on GitHub with detailed error information

---

**Remember: It's okay to ask for help. You're not alone. 💙**
