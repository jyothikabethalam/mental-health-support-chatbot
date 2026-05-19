"""
Mental Health Support Chatbot for Students

This application provides empathetic mental health support using:
- Natural Language Processing (NLP) for understanding user emotions
- Sentiment analysis to gauge mood and emotional state
- Context-aware conversation flow that builds on previous interactions
- Targeted coping strategies for specific stressors (exams, work, relationships)
- Crisis detection and resource referrals for serious situations
- Mood tracking and visualization over time

Technical Stack:
- Streamlit: Web interface framework
- NLTK: Natural Language Toolkit for text processing
- SQLite: Local database for storing conversations
- Matplotlib/Pandas: Data visualization for mood trends
"""

# ==================== IMPORTS ====================
# These are the external libraries we need for our chatbot

import streamlit as st  # Web framework for creating the user interface
import sqlite3         # Database for storing conversation history
import nltk            # Natural Language Toolkit for text processing
from nltk.sentiment import SentimentIntensityAnalyzer  # For analyzing emotional tone
import datetime        # For timestamps and time-based operations
import random          # For selecting random responses to make conversations feel natural
import re              # Regular expressions for text pattern matching

# ==================== NLP SETUP ====================
# Download the VADER (Valence Aware Dictionary and sEntiment Reasoner) lexicon
# This is a pre-trained model that can analyze the emotional tone of text
# 'quiet=True' prevents it from printing download messages
nltk.download('vader_lexicon', quiet=True)

# Initialize the sentiment analyzer
# This will be used to determine if user messages are positive, negative, or neutral
# VADER is specifically good for social media text and informal language
sia = SentimentIntensityAnalyzer()

# ==================== DATABASE SETUP ====================
# SQLite is a lightweight database that stores data in a single file
# Perfect for local applications like this chatbot

# Connect to the database file (creates it if it doesn't exist)
conn = sqlite3.connect('chatbot.db')
c = conn.cursor()  # Cursor object lets us execute SQL commands

# Create the main table for storing conversations
# This table will track:
# - id: Unique identifier for each conversation entry
# - timestamp: When the conversation happened
# - user_message: What the user said
# - bot_response: How the chatbot responded
# - sentiment: Emotional score of the user's message (-1 to +1)
c.execute('''CREATE TABLE IF NOT EXISTS mood_tracking (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT,
    user_message TEXT,
    bot_response TEXT,
    sentiment REAL
)''')

# Add conversation context column for enhanced features
# We use try/except because this column might already exist
# This demonstrates backward compatibility - making sure old databases still work
try:
    c.execute('ALTER TABLE mood_tracking ADD COLUMN conversation_context TEXT')
    conn.commit()  # Save changes to database
except sqlite3.OperationalError:
    # Column already exists or other error - that's okay, continue
    pass

# Commit all changes to make sure they're saved
conn.commit()

# ==================== RESPONSE TEMPLATES ====================
# These are pre-written responses that the chatbot can use
# Having multiple options makes conversations feel more natural and less robotic

# Greeting responses for when users first start chatting
# These are warm and welcoming to make users feel comfortable
GREETING_RESPONSES = [
    "Hello! I'm here to support you. How are you feeling today?",
    "Hi there! Thanks for reaching out. What's on your mind?",
    "Welcome! I'm glad you're here. How can I help you today?",
    "Hello! It takes courage to seek support. How are things going for you?"
]

# Empathetic responses organized by emotion type
# This dictionary structure allows us to give appropriate responses based on detected emotions
# Each emotion has multiple response options to avoid repetition
EMPATHY_RESPONSES = {
    # Responses for when users express stress
    'stress': [
        "Stress can feel overwhelming. What's been weighing on your mind lately?",
        "It sounds like you're carrying a lot right now. Would you like to talk about what's causing this stress?",
        "Feeling stressed is completely normal. What situation is making you feel this way?"
    ],
    # Responses for anxiety-related messages
    'anxiety': [
        "Anxiety can be really challenging. Can you tell me more about what's making you feel anxious?",
        "I hear that you're feeling anxious. What thoughts are going through your mind right now?",
        "Anxiety affects many people. What triggers these feelings for you?"
    ],
    # Responses for sadness and depression
    'sadness': [
        "I'm sorry you're feeling sad. Sometimes it helps to talk about what's bothering you. What's going on?",
        "Sadness is a natural emotion, but it can be hard to bear. What's been making you feel this way?",
        "It's okay to feel sad. Would you like to share what's been troubling you?"
    ],
    # General supportive responses when we can't identify specific emotions
    'general': [
        "I'm here to listen without judgment. What would you like to talk about?",
        "Thank you for sharing with me. How can I best support you right now?",
        "It's brave of you to reach out. What's been on your mind lately?"
    ]
}

COPING_STRATEGIES = {
    'breathing': [
        "Try the 4-7-8 breathing technique: Inhale for 4 counts, hold for 7, exhale for 8. This can help calm your nervous system.",
        "Focus on your breath. Take slow, deep breaths in through your nose and out through your mouth.",
        "Try box breathing: Breathe in for 4, hold for 4, out for 4, hold for 4. Repeat this cycle."
    ],
    'grounding': [
        "Try the 5-4-3-2-1 technique: Name 5 things you see, 4 you can touch, 3 you hear, 2 you smell, 1 you taste.",
        "Ground yourself by focusing on your physical sensations. Feel your feet on the floor, your back against the chair.",
        "Look around and name objects in your environment. This can help bring you back to the present moment."
    ],
    'movement': [
        "Even a 5-minute walk can help shift your mood and energy. Fresh air can be especially helpful.",
        "Try some gentle stretching or yoga poses. Movement can help release tension.",
        "Consider doing some jumping jacks or push-ups to release built-up stress energy."
    ],
    'social': [
        "Reach out to someone you trust - a friend, family member, or counselor. Connection can be healing.",
        "Consider joining a support group or online community where you can share your experiences.",
        "Sometimes just talking to someone, even briefly, can help you feel less alone."
    ],
    'self_care': [
        "Take a warm bath or shower. The physical comfort can help soothe emotional distress.",
        "Listen to music that makes you feel calm or uplifted. Music can be a powerful mood regulator.",
        "Try journaling your thoughts and feelings. Writing can help you process what you're experiencing."
    ]
}

# Specific remedies for common stressors
SPECIFIC_REMEDIES = {
    'exam_anxiety': [
        "📚 **Study Strategy:** Break your study material into small, manageable chunks. Study for 25 minutes, then take a 5-minute break (Pomodoro Technique).",
        "🧘 **Before Exam:** Practice deep breathing. Arrive early, avoid discussing the exam with anxious classmates, and remind yourself that you've prepared.",
        "💭 **Reframe Thoughts:** Replace 'I'm going to fail' with 'I've prepared as best I can, and I'll do my best.' One exam doesn't define your worth.",
        "📝 **During Exam:** Read questions carefully, start with easier questions to build confidence, and if you feel overwhelmed, pause and take 3 deep breaths."
    ],
    'work_stress': [
        "📋 **Prioritize Tasks:** Make a list and tackle the most important tasks first. Break large projects into smaller, actionable steps.",
        "⏰ **Time Management:** Use time-blocking to focus on one task at a time. Set boundaries between work and personal time.",
        "🗣️ **Communication:** If workload is overwhelming, have an honest conversation with your supervisor about priorities and deadlines.",
        "🚶 **Micro-breaks:** Take 2-minute breaks every hour to stretch, breathe, or step outside."
    ],
    'relationship_stress': [
        "💬 **Communication:** Use 'I' statements to express feelings without blaming. 'I feel...' instead of 'You always...'",
        "🤝 **Set Boundaries:** It's okay to say no and protect your emotional energy. Healthy relationships respect boundaries.",
        "🔄 **Take Space:** If emotions are high, take a break from the conversation and return when you're calmer.",
        "❤️ **Self-Compassion:** Remember that you can't control others' actions, only your responses. Focus on what you can change."
    ],
    'family_stress': [
        "🏠 **Create Safe Spaces:** Identify places or times where you can decompress away from family tension.",
        "👂 **Active Listening:** Try to understand family members' perspectives, even if you disagree with their actions.",
        "🚪 **Healthy Distance:** It's okay to limit contact with family members who consistently affect your mental health negatively.",
        "🤝 **Seek Support:** Talk to friends, counselors, or support groups about family dynamics. You're not alone."
    ],
    'general_anxiety': [
        "🧘 **Mindfulness:** Practice the 4-7-8 breathing technique when you feel anxiety rising.",
        "📱 **Limit News/Social Media:** Constant negative information can increase anxiety. Set specific times to check news.",
        "🏃 **Physical Activity:** Even 10 minutes of movement can reduce anxiety. Try walking, dancing, or stretching.",
        "💤 **Sleep Hygiene:** Anxiety often worsens with poor sleep. Aim for 7-8 hours and avoid screens before bed."
    ],
    'depression_feelings': [
        "☀️ **Light Exposure:** Spend time in natural light, especially in the morning. Open curtains or step outside.",
        "🎯 **Small Goals:** Set tiny, achievable goals like 'brush teeth' or 'make bed.' Small wins build momentum.",
        "🤝 **Social Connection:** Reach out to one person, even if it's just a text. Depression thrives in isolation.",
        "🏥 **Professional Help:** If feelings persist for more than 2 weeks, consider talking to a counselor or doctor."
    ]
}

FOLLOW_UP_QUESTIONS = [
    "How long have you been feeling this way?",
    "What do you think might have triggered these feelings?",
    "Have you tried any coping strategies before? What worked or didn't work?",
    "Is there anything specific you'd like help with right now?",
    "What would make you feel a little bit better today?",
    "Are you getting enough sleep and taking care of your basic needs?"
]

CRISIS_KEYWORDS = [
    "suicide", "kill myself", "end it all", "can't go on", "want to die", 
    "self-harm", "hurt myself", "cutting", "hopeless", "worthless", 
    "no point", "better off dead", "end my life"
]

CRISIS_RESPONSE = """I'm really concerned about you and want you to know that you're not alone. These feelings can be overwhelming, but there is help available.

🆘 **Immediate Resources:**
- **Crisis Text Line:** Text HOME to 741741
- **National Suicide Prevention Lifeline:** 988
- **Emergency Services:** 911

Please consider reaching out to a mental health professional, trusted friend, or family member right now. Your life has value, and there are people who want to help you through this difficult time.

Would you like me to help you find local mental health resources?"""

# ==================== HELPER FUNCTIONS ====================
# These functions handle the core logic of understanding and responding to users

def detect_crisis(message):
    """
    Detect if a user message contains crisis-related keywords.
    
    This is a critical safety feature that identifies when someone might be
    in immediate danger or having thoughts of self-harm.
    
    Args:
        message (str): The user's message to analyze
        
    Returns:
        bool: True if crisis keywords are detected, False otherwise
        
    How it works:
    1. Convert message to lowercase for case-insensitive matching
    2. Check if ANY crisis keyword appears in the message
    3. Return True immediately if found (this triggers crisis response)
    """
    message_lower = message.lower()
    # The 'any()' function returns True if ANY item in the list is True
    # This checks each crisis keyword to see if it appears in the message
    return any(keyword in message_lower for keyword in CRISIS_KEYWORDS)

def get_sentiment(message):
    """
    Analyze the emotional tone of a message using VADER sentiment analysis.
    
    Args:
        message (str): The user's message to analyze
        
    Returns:
        float: Sentiment score from -1 (very negative) to +1 (very positive)
               0 is neutral
    
    How VADER works:
    - It looks at individual words and their emotional associations
    - It considers context like capitalization ("GREAT" vs "great")
    - It handles negations ("not good" vs "good")
    - It accounts for punctuation ("Good!" vs "Good")
    
    The 'compound' score is a normalized summary of all sentiment indicators
    """
    # Get all sentiment scores from VADER
    scores = sia.polarity_scores(message)
    # Return the compound score - this is the overall sentiment
    # Positive values = positive sentiment, negative values = negative sentiment
    return scores['compound']

def detect_emotion_keywords(message):
    """
    Identify specific emotions mentioned in the user's message.
    
    This function looks for emotion-related keywords to understand what
    the user is feeling, which helps us provide more targeted support.
    
    Args:
        message (str): The user's message to analyze
        
    Returns:
        list: List of detected emotions (can be multiple)
        
    Example:
        detect_emotion_keywords("I'm stressed and anxious about my exam")
        Returns: ['stress', 'anxiety']
    """
    message_lower = message.lower()
    
    # Dictionary mapping emotion categories to related keywords
    # Each emotion has multiple keywords to catch different ways people express feelings
    emotions = {
        'stress': ['stress', 'stressed', 'overwhelmed', 'pressure', 'burden'],
        'anxiety': ['anxious', 'anxiety', 'worried', 'nervous', 'panic', 'fear'],
        'sadness': ['sad', 'depressed', 'down', 'upset', 'crying', 'tears'],
        'anger': ['angry', 'mad', 'frustrated', 'irritated', 'furious'],
        'loneliness': ['lonely', 'alone', 'isolated', 'disconnected']
    }
    
    detected = []  # List to store found emotions
    
    # Check each emotion category
    for emotion, keywords in emotions.items():
        # If ANY keyword for this emotion is found in the message
        if any(keyword in message_lower for keyword in keywords):
            detected.append(emotion)  # Add this emotion to our list
    
    return detected

def detect_specific_stressors(message):
    """
    Identify specific types of stressors mentioned in the message.
    
    This function recognizes common stressor categories so we can provide
    targeted, practical advice rather than generic responses.
    
    Args:
        message (str): The user's message to analyze
        
    Returns:
        list: List of detected stressor types
        
    Why this matters:
    Someone stressed about exams needs different advice than someone
    stressed about work or relationships. This function helps us
    provide relevant, actionable coping strategies.
    """
    message_lower = message.lower()
    
    # Dictionary mapping stressor types to related keywords
    # Each category represents a different area of life stress
    stressors = {
        # Academic stress - very common among students
        'exam_anxiety': ['exam', 'test', 'quiz', 'midterm', 'final', 'study', 'studying', 'grade', 'fail'],
        
        # Work-related stress
        'work_stress': ['work', 'job', 'boss', 'colleague', 'deadline', 'project', 'meeting', 'workload'],
        
        # Relationship difficulties
        'relationship_stress': ['relationship', 'partner', 'boyfriend', 'girlfriend', 'dating', 'breakup'],
        
        # Family problems
        'family_stress': ['family', 'parent', 'mom', 'dad', 'mother', 'father', 'sibling', 'brother', 'sister'],
        
        # General anxiety symptoms
        'general_anxiety': ['anxiety', 'anxious', 'worried', 'panic', 'fear'],
        
        # Depression-related feelings
        'depression_feelings': ['useless', 'worthless', 'hopeless', 'depressed', 'sad', 'empty']
    }
    
    detected = []  # List to store found stressor types
    
    # Check each stressor category
    for stressor, keywords in stressors.items():
        # If ANY keyword for this stressor is found
        if any(keyword in message_lower for keyword in keywords):
            detected.append(stressor)
    
    return detected

def analyze_conversation_context(conversation_history):
    """
    Analyze recent conversation history to understand context and avoid repetition.
    
    This function is crucial for making conversations feel natural and progressive.
    It prevents the chatbot from asking the same questions repeatedly and helps
    build on previous conversations.
    
    Args:
        conversation_history (list): List of (user_message, bot_response) tuples
        
    Returns:
        dict: Context information including:
            - topics_discussed: What life areas have been mentioned
            - questions_asked: What questions the bot has already asked
            - emotions_mentioned: What emotions have been discussed
            - is_first_interaction: Whether this is the user's first message
    
    Why this matters:
    Without context awareness, chatbots feel robotic and repetitive.
    This function makes conversations feel more human and progressive.
    """
    # If no conversation history, this is the first interaction
    if not conversation_history:
        return {
            'topics_discussed': [], 
            'questions_asked': [], 
            'emotions_mentioned': [], 
            'is_first_interaction': True
        }
    
    # Initialize lists to track conversation elements
    topics_discussed = []
    questions_asked = []
    emotions_mentioned = []
    
    # Analyze the last 3 conversation exchanges (to avoid going too far back)
    for user_msg, bot_msg in conversation_history[:3]:
        # Extract topics from user messages
        # This helps us understand what areas of life the user is struggling with
        user_lower = user_msg.lower()
        
        # Check for academic-related topics
        if any(word in user_lower for word in ['exam', 'test', 'study', 'school', 'college']):
            topics_discussed.append('academic')
        
        # Check for work-related topics
        if any(word in user_lower for word in ['work', 'job', 'boss', 'colleague']):
            topics_discussed.append('work')
        
        # Check for family-related topics
        if any(word in user_lower for word in ['family', 'parent', 'mom', 'dad', 'sibling']):
            topics_discussed.append('family')
        
        # Check for relationship topics
        if any(word in user_lower for word in ['friend', 'relationship', 'partner']):
            topics_discussed.append('relationships')
        
        # Extract emotions that have been mentioned
        # This helps us avoid repeatedly asking about the same emotions
        emotions_mentioned.extend(detect_emotion_keywords(user_msg))
        
        # Analyze what questions the bot has already asked
        # This prevents repetitive questioning
        bot_lower = bot_msg.lower()
        
        if 'how long' in bot_lower:
            questions_asked.append('duration')
        if 'what triggered' in bot_lower or 'what caused' in bot_lower:
            questions_asked.append('triggers')
        if 'tried any coping' in bot_lower:
            questions_asked.append('coping_history')
        if 'getting enough sleep' in bot_lower:
            questions_asked.append('self_care')
    
    # Return context information
    # We use set() to remove duplicates, then convert back to list
    return {
        'topics_discussed': list(set(topics_discussed)),
        'questions_asked': list(set(questions_asked)),
        'emotions_mentioned': list(set(emotions_mentioned)),
        'is_first_interaction': False
    }

def get_contextual_response(message, sentiment, conversation_history):
    """
    Generate an intelligent, contextual response based on the user's message,
    emotional state, and conversation history.
    
    This is the "brain" of the chatbot - it decides how to respond based on:
    1. What the user just said (message content)
    2. The emotional tone of their message (sentiment)
    3. What we've talked about before (conversation history)
    4. Specific stressors or emotions detected
    
    Args:
        message (str): The user's current message
        sentiment (float): Sentiment score from -1 to +1
        conversation_history (list): Previous conversation exchanges
        
    Returns:
        str: The chatbot's response
        
    Response Priority (in order):
    1. Crisis detection (highest priority - safety first)
    2. Specific stressor remedies (practical help)
    3. Emotion-based responses (empathy + coping strategies)
    4. General supportive responses (fallback)
    """
    # Detect emotions and stressors in the current message
    emotions = detect_emotion_keywords(message)
    context = analyze_conversation_context(conversation_history)
    
    # PRIORITY 1: Handle greetings and first interactions
    # Make users feel welcome and comfortable from the start
    if context['is_first_interaction'] or any(greeting in message.lower() for greeting in ['hello', 'hi', 'hey']):
        return random.choice(GREETING_RESPONSES)
    
    # PRIORITY 2: Crisis detection takes absolute priority
    # Safety is our top concern - if someone is in crisis, respond immediately
    if detect_crisis(message):
        return CRISIS_RESPONSE
    
    # Build contextual response based on conversation history
    message_lower = message.lower()
    
    # If user is answering a previous question, acknowledge and build on it
    if any(word in message_lower for word in ['because', 'since', 'started', 'began', 'ago', 'when']):
        acknowledgments = [
            "Thank you for sharing that with me. ",
            "I appreciate you opening up about this. ",
            "That helps me understand better. "
        ]
        response = random.choice(acknowledgments)
        
        # Follow up based on what they shared
        if sentiment < -0.3:
            response += "That sounds really challenging. How are you coping with this situation?"
        else:
            response += "How has this been affecting your daily life?"
        
        return response
    
    # If user is expressing a new concern, acknowledge the pattern
    if len(context['emotions_mentioned']) > 1:
        response = "I notice you've been dealing with multiple challenges. "
        if sentiment < -0.4:
            response += "It's understandable to feel overwhelmed when facing several difficulties at once. What feels most pressing to you right now?"
        else:
            response += "You're handling a lot. What's been helping you get through these tough times?"
        return response
    
    # PRIORITY 3: Check for specific stressors and provide targeted remedies
    # This is where we become solution-focused rather than just asking questions
    stressors = detect_specific_stressors(message)
    if stressors:
        primary_stressor = stressors[0]  # Focus on the first detected stressor
        
        # Provide empathetic acknowledgment + immediate practical remedy
        # Each stressor type gets specific, actionable advice
        
        if primary_stressor == 'exam_anxiety':
            # Students need practical study strategies and test-taking tips
            response = "Exam anxiety is really common and completely understandable. Here are some strategies that can help:\n\n"
            response += random.choice(SPECIFIC_REMEDIES['exam_anxiety'])
            response += "\n\nWould you like more study strategies or relaxation techniques?"
            
        elif primary_stressor == 'work_stress':
            # Work stress needs time management and communication strategies
            response = "Work stress can be overwhelming. Let me share some practical strategies:\n\n"
            response += random.choice(SPECIFIC_REMEDIES['work_stress'])
            response += "\n\nWould you like more tips for managing workplace stress?"
            
        elif primary_stressor == 'relationship_stress':
            # Relationship issues need communication and boundary-setting advice
            response = "Relationship challenges can be emotionally draining. Here's something that might help:\n\n"
            response += random.choice(SPECIFIC_REMEDIES['relationship_stress'])
            response += "\n\nWould you like to talk more about what's happening in your relationship?"
            
        elif primary_stressor == 'family_stress':
            # Family stress needs boundary-setting and self-care strategies
            response = "Family dynamics can be really challenging. Here's a strategy that might help:\n\n"
            response += random.choice(SPECIFIC_REMEDIES['family_stress'])
            response += "\n\nFamily stress can be complex. How are you taking care of yourself through this?"
            
        elif primary_stressor == 'depression_feelings':
            # Depression needs gentle encouragement and professional resource referrals
            response = "I hear that you're struggling with these difficult feelings. You're not alone, and these feelings don't define your worth. Here's something that might help:\n\n"
            response += random.choice(SPECIFIC_REMEDIES['depression_feelings'])
            response += "\n\nRemember, if these feelings persist, it's important to reach out to a mental health professional."
            
        else:  # general_anxiety
            # General anxiety needs immediate calming techniques
            response = "Anxiety can feel overwhelming, but there are effective ways to manage it:\n\n"
            response += random.choice(SPECIFIC_REMEDIES['general_anxiety'])
            response += "\n\nWould you like to try a quick breathing exercise together?"
        
        return response
    
    # Respond based on detected emotions, avoiding repeated questions
    if emotions:
        primary_emotion = emotions[0]
        
        # If we've already discussed this emotion, provide coping strategies
        if primary_emotion in context['emotions_mentioned']:
            response = "I notice you're still dealing with these challenging feelings. Let me suggest a coping strategy that might help:\n\n"
            strategy = get_coping_strategy(primary_emotion)
            response += f"💡 **{strategy}**\n\nHow does this feel for you? Would you like to try this or explore other options?"
            return response
        
        # New emotion - provide empathy + immediate strategy
        if primary_emotion in EMPATHY_RESPONSES:
            response = random.choice(EMPATHY_RESPONSES[primary_emotion])
            response += "\n\nLet me share a coping strategy that might help:\n\n"
            strategy = get_coping_strategy(primary_emotion)
            response += f"💡 **{strategy}**"
        else:
            response = random.choice(EMPATHY_RESPONSES['general'])
    else:
        # Sentiment-based responses, avoiding repeated questions
        available_questions = [q for q in FOLLOW_UP_QUESTIONS if not any(keyword in q.lower() for keyword in context['questions_asked'])]
        
        if sentiment < -0.5:
            response = "I can hear that you're going through a really tough time. "
            if available_questions:
                response += random.choice(available_questions)
            else:
                response += "What would help you feel even a little bit better right now?"
        elif sentiment < -0.1:
            response = "It sounds like things are challenging right now. "
            if available_questions:
                response += random.choice(available_questions)
            else:
                response += "What's one small thing that might help you today?"
        elif sentiment > 0.3:
            response = "I'm glad to hear some positivity in your message! "
            response += "What's been going well for you lately?"
        else:
            if available_questions:
                response = random.choice(EMPATHY_RESPONSES['general']) + " " + random.choice(available_questions)
            else:
                response = "I'm here to listen. What's most important for you to talk about right now?"
    
    return response

def get_coping_strategy(emotion_type=None):
    """Get a relevant coping strategy based on emotion type"""
    if emotion_type in ['stress', 'anxiety']:
        strategy_type = random.choice(['breathing', 'grounding', 'movement'])
    elif emotion_type == 'sadness':
        strategy_type = random.choice(['self_care', 'social', 'movement'])
    else:
        strategy_type = random.choice(list(COPING_STRATEGIES.keys()))
    
    return random.choice(COPING_STRATEGIES[strategy_type])

def save_interaction(user_message, bot_response, sentiment, context=""):
    timestamp = datetime.datetime.now().isoformat()
    c.execute('INSERT INTO mood_tracking (timestamp, user_message, bot_response, sentiment, conversation_context) VALUES (?, ?, ?, ?, ?)',
              (timestamp, user_message, bot_response, sentiment, context))
    conn.commit()

def get_mood_history():
    c.execute('SELECT timestamp, sentiment FROM mood_tracking ORDER BY timestamp DESC LIMIT 20')
    return c.fetchall()

def get_conversation_history():
    c.execute('SELECT user_message, bot_response FROM mood_tracking ORDER BY timestamp DESC LIMIT 5')
    return c.fetchall()

def get_recent_user_messages():
    """Get recent user messages for context analysis"""
    c.execute('SELECT user_message FROM mood_tracking ORDER BY timestamp DESC LIMIT 3')
    return [row[0] for row in c.fetchall()]

# ==================== STREAMLIT USER INTERFACE ====================
# Streamlit is a Python framework that makes it easy to create web apps
# All the st.* functions create different UI elements

# Configure the web page settings
st.set_page_config(
    page_title="Student Mental Health Chatbot",  # Shows in browser tab
    page_icon="💬",  # Icon in browser tab
    layout="wide"  # Use full width of screen
)

# Custom CSS styling to make the chat interface look better
# This CSS creates styled chat bubbles for user and bot messages
st.markdown("""
<style>
.chat-message {
    padding: 1rem; border-radius: 0.5rem; margin-bottom: 1rem; display: flex
}
.chat-message.user {
    background-color: #2b313e  /* Dark blue for user messages */
}
.chat-message.bot {
    background-color: #475063  /* Lighter blue for bot messages */
}
.chat-message .message {
    width: 80%; padding: 0 1rem; color: #fff;  /* White text */
}
</style>
""", unsafe_allow_html=True)

# Main title and welcome message
st.title("💬 Student Mental Health Support Chatbot")
st.markdown("**I'm here to listen and support you. This is a safe, private, and non-judgmental space.**")

# ==================== SESSION STATE MANAGEMENT ====================
# Streamlit "session state" keeps data persistent across user interactions
# Without this, the app would forget everything when the user sends a message

# Initialize chat history - stores all conversation exchanges
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []  # List of (user_msg, bot_msg, sentiment) tuples

# Track whether to show coping strategies
if 'show_coping_strategies' not in st.session_state:
    st.session_state.show_coping_strategies = False

# Count total messages in this session
if 'conversation_count' not in st.session_state:
    st.session_state.conversation_count = 0

# Main chat interface
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("💭 Chat")
    
    # Chat input
    user_input = st.text_input("Share what's on your mind...", key="user_input")
    
    col_send, col_coping = st.columns([1, 1])
    
    with col_send:
        send_clicked = st.button("Send Message", type="primary")
    
    with col_coping:
        coping_clicked = st.button("Get Coping Strategy")
    
    # Process user input
    if send_clicked and user_input:
        conversation_history = get_conversation_history()
        sentiment = get_sentiment(user_input)
        emotions = detect_emotion_keywords(user_input)
        
        # Generate contextual response
        bot_response = get_contextual_response(user_input, sentiment, conversation_history)
        
        # Save interaction
        context = f"emotions: {emotions}, sentiment: {sentiment:.2f}"
        save_interaction(user_input, bot_response, sentiment, context)
        
        # Add to chat history
        st.session_state.chat_history.append((user_input, bot_response, sentiment))
        st.session_state.conversation_count += 1
        
        # Offer coping strategies for negative emotions
        if sentiment < -0.2 or any(emotion in ['stress', 'anxiety', 'sadness'] for emotion in emotions):
            st.session_state.show_coping_strategies = True
    
    # Handle coping strategy request
    if coping_clicked:
        recent_emotions = []
        if st.session_state.chat_history:
            last_message = st.session_state.chat_history[-1][0]
            recent_emotions = detect_emotion_keywords(last_message)
        
        emotion_type = recent_emotions[0] if recent_emotions else None
        strategy = get_coping_strategy(emotion_type)
        
        st.session_state.chat_history.append(("[Requested coping strategy]", f"💡 **Coping Strategy:** {strategy}", 0))
    
    # Display chat history
    st.markdown("---")
    if st.session_state.chat_history:
        for i, (user_msg, bot_msg, sentiment) in enumerate(st.session_state.chat_history[-8:]):
            # User message
            st.markdown(f'<div class="chat-message user"><div class="message"><strong>You:</strong> {user_msg}</div></div>', unsafe_allow_html=True)
            
            # Bot message with sentiment indicator
            sentiment_emoji = "😊" if sentiment > 0.2 else "😐" if sentiment > -0.2 else "😔"
            st.markdown(f'<div class="chat-message bot"><div class="message"><strong>Support Bot {sentiment_emoji}:</strong> {bot_msg}</div></div>', unsafe_allow_html=True)
    else:
        st.info("👋 Hello! I'm here to support you. Feel free to share what's on your mind, whether you're feeling stressed, anxious, sad, or just need someone to talk to.")

with col2:
    st.subheader("📊 Your Wellbeing")
    
    # Mood tracking visualization
    history = get_mood_history()
    if history and len(history) > 1:
        import pandas as pd
        import matplotlib.pyplot as plt
        
        df = pd.DataFrame(history, columns=["timestamp", "sentiment"])
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df = df.sort_values('timestamp')
        
        # Create mood trend chart
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.plot(df['timestamp'], df['sentiment'], marker='o', linewidth=2, markersize=4)
        ax.axhline(y=0, color='gray', linestyle='--', alpha=0.5)
        ax.set_ylabel('Mood Score')
        ax.set_title('Your Mood Trend')
        ax.grid(True, alpha=0.3)
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        st.pyplot(fig)
        
        # Mood insights
        avg_mood = df['sentiment'].mean()
        if avg_mood > 0.1:
            st.success(f"💚 Your average mood has been positive ({avg_mood:.2f})")
        elif avg_mood > -0.1:
            st.info(f"💛 Your mood has been neutral ({avg_mood:.2f})")
        else:
            st.warning(f"💙 Your mood has been challenging ({avg_mood:.2f}). Remember, it's okay to seek support.")
    else:
        st.info("Start chatting to see your mood trends!")
    
    # Quick resources
    st.subheader("🆘 Quick Resources")
    st.markdown("""
    **Crisis Support:**
    - 🆘 Crisis Text Line: Text HOME to 741741
    - 📞 National Suicide Prevention Lifeline: 988
    - 🚨 Emergency: 911
    
    **Self-Care Reminders:**
    - 💧 Stay hydrated
    - 😴 Get adequate sleep
    - 🚶‍♀️ Take breaks and move
    - 🤝 Connect with others
    """)
    
    # Session stats
    if st.session_state.conversation_count > 0:
        st.subheader("📈 Session Stats")
        st.metric("Messages Exchanged", st.session_state.conversation_count)
        
        if st.button("Clear Chat History"):
            st.session_state.chat_history = []
            st.session_state.conversation_count = 0
            st.rerun()

# Mood tracking visualization
st.subheader("Your Recent Mood Trends")
history = get_mood_history()
if history:
    import pandas as pd
    import matplotlib.pyplot as plt
    df = pd.DataFrame(history, columns=["timestamp", "sentiment"])
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df = df.sort_values('timestamp')
    st.line_chart(df.set_index('timestamp')['sentiment'])
else:
    st.write("No mood data yet. Start chatting to track your mood!")

st.caption("This chatbot is not a substitute for professional therapy. In a crisis, please reach out to a professional or call 988.")
