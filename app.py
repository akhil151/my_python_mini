import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime
import time
from transformers import pipeline

# Set page configuration
st.set_page_config(
    page_title="Emotion-Based Mental Health Helper",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for professional UI
st.markdown("""
<style>
    /* Global Styling */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
    
    * {
        font-family: 'Poppins', sans-serif;
    }
    
    .main {
        background-color: #f9fafb;
        padding: 2rem;
    }
    
    /* Header Styling */
    h1, h2, h3, h4 {
        color: #1e293b;
        font-weight: 600;
    }
    
    h1 {
        font-size: 2.5rem !important;
        margin-bottom: 1.5rem !important;
        background: linear-gradient(90deg, #3b82f6, #8b5cf6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        display: inline-block;
    }
    
    /* Card Styling */
    .card {
        background-color: white;
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
        margin-bottom: 2rem;
        border-top: 4px solid #3b82f6;
    }
    
    .card-header {
        font-size: 1.25rem;
        font-weight: 600;
        margin-bottom: 1rem;
        padding-bottom: 0.75rem;
        border-bottom: 1px solid #e5e7eb;
        color: #1e293b;
    }
    
    /* Input Styling */
    .stTextInput>div>div>input, .stTextArea>div>div>textarea {
        font-size: 16px;
        padding: 12px 16px;
        border-radius: 8px;
        border: 1px solid #d1d5db;
        box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
        transition: all 0.3s;
    }
    
    .stTextInput>div>div>input:focus, .stTextArea>div>div>textarea:focus {
        border-color: #3b82f6;
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.3);
    }
    
    /* Button Styling */
    .stButton>button {
        background: linear-gradient(90deg, #3b82f6, #8b5cf6);
        color: white;
        font-weight: 500;
        padding: 0.75rem 1.5rem;
        border-radius: 8px;
        border: none;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px -1px rgba(59, 130, 246, 0.2), 0 2px 4px -1px rgba(59, 130, 246, 0.1);
        width: 100%; 
        font-size: 16px;
    }
    
    .stButton>button:hover {
        background: linear-gradient(90deg, #2563eb, #7c3aed);
        transform: translateY(-2px);
        box-shadow: 0 10px 15px -3px rgba(59, 130, 246, 0.3), 0 4px 6px -2px rgba(59, 130, 246, 0.2);
    }
    
    .stButton>button:active {
        transform: translateY(0);
    }
    
    /* Emotion Cards */
    .emotion-card {
        background-color: white;
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
        border-left: 6px solid #3b82f6;
        transition: transform 0.3s ease;
    }
    
    .emotion-card:hover {
        transform: translateY(-5px);
    }
    
    /* Emotion Log Item */
    .emotion-log-item {
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 0.75rem;
        background-color: white;
        border-left: 4px solid #3b82f6;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.06);
        transition: all 0.2s;
    }
    
    .emotion-log-item:hover {
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        transform: translateX(3px);
    }
    
    /* Callout Box */
    .highlight {
        background: linear-gradient(135deg, rgba(59, 130, 246, 0.1), rgba(139, 92, 246, 0.1));
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1.5rem 0;
        border: 1px solid rgba(59, 130, 246, 0.2);
        position: relative;
    }
    
    .highlight:before {
        content: "💡";
        font-size: 1.5rem;
        position: absolute;
        top: -15px;
        left: 20px;
        background-color: #f9fafb;
        padding: 0 10px;
    }
    
    /* Progress Bars */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #3b82f6, #8b5cf6);
    }
    
    /* Sidebar */
    .css-1d391kg {
        background-color: #f1f5f9;
    }
    
    /* Layout Helpers */
    .flex-container {
        display: flex;
        gap: 1rem;
    }
    
    .divider {
        height: 1px;
        background-color: #e5e7eb;
        margin: 1.5rem 0;
    }
    
    /* Badges */
    .badge {
        padding: 0.25rem 0.75rem;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 500;
        background-color: #e5e7eb;
        color: #1f2937;
        display: inline-block;
        margin-right: 0.5rem;
    }
    
    .badge-blue {
        background-color: rgba(59, 130, 246, 0.1);
        color: #1d4ed8;
    }
    
    .badge-purple {
        background-color: rgba(139, 92, 246, 0.1);
        color: #6d28d9;
    }
    
    .badge-green {
        background-color: rgba(16, 185, 129, 0.1);
        color: #065f46;
    }
    
    /* Animation */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .animate-fade-in {
        animation: fadeIn 0.5s ease forwards;
    }
    
    /* Table Styling */
    .dataframe {
        border-collapse: collapse;
        width: 100%;
        border-radius: 8px;
        overflow: hidden;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .dataframe th {
        background-color: #f3f4f6;
        padding: 0.75rem 1rem;
        text-align: left;
        font-weight: 600;
        color: #374151;
        border-bottom: 2px solid #e5e7eb;
    }
    
    .dataframe td {
        padding: 0.75rem 1rem;
        border-bottom: 1px solid #e5e7eb;
    }
    
    .dataframe tr:hover {
        background-color: #f9fafb;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state for storing emotion history
if 'emotion_history' not in st.session_state:
    st.session_state.emotion_history = []

# Load the emotion classifier
@st.cache_resource
def load_emotion_model():
    with st.spinner("Loading emotion detection model..."):
        emotion_classifier = pipeline("text-classification", 
                                      model="j-hartmann/emotion-english-distilroberta-base", 
                                      return_all_scores=True)
    return emotion_classifier

emotion_classifier = load_emotion_model()

# Dictionary mapping emotions to emojis, colors and wellness tips
emotion_map = {
    "joy": {
        "emoji": "😊",
        "color": "#10b981",  # Green
        "tips": [
            "Wonderful! Share your joy with someone else today.",
            "Take a moment to appreciate what's going well in your life.",
            "Consider journaling about this positive feeling to reflect on later.",
            "Use this positive energy to tackle a task you've been putting off.",
            "Good emotions are worth celebrating - maybe treat yourself today!"
        ]
    },
    "sadness": {
        "emoji": "😢",
        "color": "#60a5fa",  # Blue
        "tips": [
            "It's okay to feel sad. Give yourself permission to experience your emotions.",
            "Try deep breathing for 5 minutes - inhale for 4 seconds, hold for 2, exhale for 6.",
            "Consider reaching out to a friend or family member you trust.",
            "A short walk outside might help shift your perspective.",
            "Hydrate and make sure you've eaten something nourishing today."
        ]
    },
    "anger": {
        "emoji": "😠",
        "color": "#ef4444",  # Red
        "tips": [
            "When angry, try counting slowly to 10 before responding.",
            "Physical activity can help release tension - even a quick stretch.",
            "Writing down what's bothering you might help organize your thoughts.",
            "Consider if your anger is proportional to the situation.",
            "Deep breathing can help calm your nervous system when feeling angry."
        ]
    },
    "fear": {
        "emoji": "😨",
        "color": "#a78bfa",  # Purple
        "tips": [
            "Remember that you've overcome difficult situations before.",
            "Try grounding yourself: name 5 things you can see, 4 you can touch, 3 you can hear, 2 you can smell, and 1 you can taste.",
            "Break what's scaring you into smaller, manageable steps.",
            "Uncertainty is part of life - focus on what you can control.",
            "Consider writing down your fears to examine them more objectively."
        ]
    },
    "love": {
        "emoji": "❤️",
        "color": "#f87171",  # Light red
        "tips": [
            "Express your appreciation to those you care about.",
            "Love includes self-care too - do something kind for yourself today.",
            "Consider writing a gratitude list for the relationships in your life.",
            "Share your positive feelings with others around you.",
            "Use this warm feeling to reach out to someone you haven't talked to in a while."
        ]
    },
    "surprise": {
        "emoji": "😲",
        "color": "#fbbf24",  # Yellow
        "tips": [
            "Take a moment to process unexpected events before reacting.",
            "Surprises can open up new perspectives - what might you learn from this?",
            "Share your experience with someone else to help process it.",
            "Journal about this unexpected moment to reflect on later.",
            "Remember that adaptability is a strength you can develop."
        ]
    },
    "neutral": {
        "emoji": "😐",
        "color": "#9ca3af",  # Gray
        "tips": [
            "Sometimes a neutral state is a good time for reflection.",
            "Consider setting an intention for how you'd like to feel today.",
            "This might be a good time to try something new that interests you.",
            "Check in with your body - do you need water, rest, or movement?",
            "Use this balanced state to plan or organize something important to you."
        ]
    },
    "disgust": {
        "emoji": "🤢",
        "color": "#4ade80",  # Green
        "tips": [
            "Try to identify exactly what's causing this feeling.",
            "Sometimes stepping away from a situation can help provide clarity.",
            "Consider if there's something constructive you can do about what's bothering you.",
            "Your feelings are valid, even if others don't understand them.",
            "A few minutes of fresh air might help clear your mind."
        ]
    }
}

# Function to detect emotion from text
def detect_emotion(text):
    if not text.strip():
        return None
    
    # Add a loading spinner
    with st.spinner("Analyzing your emotions..."):
        result = emotion_classifier(text)
        emotions_scores = {item['label']: item['score'] for item in result[0]}
        detected_emotion = max(emotions_scores, key=emotions_scores.get)
        confidence_score = emotions_scores[detected_emotion]
        return detected_emotion, confidence_score, emotions_scores

# Function to get a random tip based on emotion
def get_tip(emotion):
    tips = emotion_map.get(emotion, emotion_map["neutral"])["tips"]
    return np.random.choice(tips)

# Function to add entry to emotion history
def add_to_history(text, emotion, tip):
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    st.session_state.emotion_history.append({
        "timestamp": now,
        "text": text,
        "emotion": emotion,
        "tip": tip
    })

# Create sidebar
with st.sidebar:
    st.markdown('<h2 style="text-align: center;">🧠 Mind Wellness</h2>', unsafe_allow_html=True)
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div style="padding: 1rem; background-color: white; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
        <h3 style="font-size: 1.2rem; margin-bottom: 0.75rem;">About This App</h3>
        <p style="font-size: 0.9rem; color: #4b5563;">
            Mind Wellness uses AI to detect emotions in your text and provide personalized supportive responses.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div style="padding: 1rem; background-color: white; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
        <h3 style="font-size: 1.2rem; margin-bottom: 0.75rem;">How It Works</h3>
        <ol style="font-size: 0.9rem; color: #4b5563; padding-left: 1.25rem;">
            <li>Share how you're feeling</li>
            <li>AI analyzes your emotional tone</li>
            <li>Receive a supportive response</li>
            <li>Track your emotional patterns</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div style="padding: 1rem; background-color: #fee2e2; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
        <h3 style="font-size: 1.2rem; margin-bottom: 0.75rem; color: #b91c1c;">Important Note</h3>
        <p style="font-size: 0.9rem; color: #b91c1c;">
            This is not a substitute for professional mental health support. If you're experiencing serious mental health issues, please contact a mental health professional.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div style="padding: 1rem; background-color: white; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
        <h3 style="font-size: 1.2rem; margin-bottom: 0.75rem;">Resources</h3>
        <ul style="font-size: 0.9rem; color: #4b5563; padding-left: 1.25rem;">
            <li>National Suicide Prevention Lifeline: 988</li>
            <li>Crisis Text Line: Text HOME to 741741</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; font-size: 0.8rem; color: #6b7280;">Created with ❤️ using Streamlit and HuggingFace</p>', unsafe_allow_html=True)

# Main content
st.markdown('<h1>🧠 Emotion-Based Mental Health Helper</h1>', unsafe_allow_html=True)

# Create two columns for main content layout
col1, col2 = st.columns([2, 1])

with col1:
    # Intro text
    st.markdown("""
    <div class="highlight animate-fade-in">
        <p style="font-size: 1.1rem; margin-bottom: 0;">
            Express how you're feeling, and I'll analyze your emotion to offer personalized supportive advice.
        </p>
        <p style="font-size: 0.8rem; color: #6b7280; margin-top: 10px;">
            Regular emotional check-ins can help improve self-awareness and mental well-being.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Input card
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-header">How are you feeling today?</div>', unsafe_allow_html=True)
    user_input = st.text_area("", height=120, 
                             placeholder="Example: I feel like I can't concentrate on anything today, and it's frustrating me...",
                             label_visibility="collapsed")
    detect_button = st.button("Analyze My Emotion")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Process input and display results
    if detect_button and user_input:
        result = detect_emotion(user_input)
        
        if result:
            detected_emotion, confidence, all_scores = result
            emoji = emotion_map.get(detected_emotion, emotion_map["neutral"])["emoji"]
            color = emotion_map.get(detected_emotion, emotion_map["neutral"])["color"]
            wellness_tip = get_tip(detected_emotion)
            
            # Add to history
            add_to_history(user_input, detected_emotion, wellness_tip)
            
            # Display results in a card with animation
            st.markdown(f"""
            <div class="emotion-card animate-fade-in" style="border-left-color: {color}">
                <h2 style="display: flex; align-items: center; gap: 10px; color: {color}">
                    <span style="font-size: 2rem;">{emoji}</span> 
                    <span>Detected Emotion: {detected_emotion.capitalize()}</span>
                </h2>
                <div style="background: linear-gradient(90deg, {color}, rgba(255,255,255,0.3)); 
                           height: 10px; border-radius: 5px; margin: 15px 0;">
                    <div style="width: {confidence*100}%; background-color: {color}; 
                              height: 100%; border-radius: 5px;"></div>
                </div>
                <p style="color: #4b5563;">Confidence: <strong>{confidence*100:.1f}%</strong></p>
            </div>
            """, unsafe_allow_html=True)
            
            # Display wellness tip with animation
            st.markdown(f"""
            <div class="emotion-card animate-fade-in" style="border-left-color: {color}">
                <h3 style="display: flex; align-items: center; gap: 10px; color: {color}">
                    <span>💡</span> 
                    <span>Personalized Support</span>
                </h3>
                <p style="font-size: 1.1rem; font-weight: 500; color: #1f2937;">{wellness_tip}</p>
                <div style="display: flex; gap: 0.5rem; margin-top: 1rem;">
                    <span class="badge badge-blue">#{detected_emotion}</span>
                    <span class="badge badge-purple">#wellness</span>
                    <span class="badge badge-green">#mindfulness</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Optional: Show emotion distribution
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown('<div class="card-header">Emotion Analysis</div>', unsafe_allow_html=True)
            df = pd.DataFrame({
                'Emotion': list(all_scores.keys()),
                'Score': list(all_scores.values())
            })
            df = df.sort_values('Score', ascending=False).reset_index(drop=True)
            
            fig = px.bar(df, x='Emotion', y='Score', color='Score',
                       color_continuous_scale='Blues', height=300)
            fig.update_layout(
                xaxis_title="", 
                yaxis_title="Confidence Score",
                margin=dict(l=20, r=20, t=30, b=20),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                xaxis=dict(
                    tickfont=dict(size=12),
                    gridcolor='#f3f4f6'
                ),
                yaxis=dict(
                    tickfont=dict(size=12),
                    gridcolor='#f3f4f6'
                )
            )
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

with col2:
    # Emotion History Section
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-header">Your Emotion Journey</div>', unsafe_allow_html=True)
    
    if st.session_state.emotion_history:
        # Display in a table
        for i, entry in enumerate(reversed(st.session_state.emotion_history[-5:])):
            emotion = entry["emotion"]
            emoji = emotion_map.get(emotion, emotion_map["neutral"])["emoji"]
            color = emotion_map.get(emotion, emotion_map["neutral"])["color"]
            
            st.markdown(f"""
            <div class="emotion-log-item" style="border-left-color: {color}">
                <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                    <span style="font-weight: 600; color: {color};">{emoji} {emotion.capitalize()}</span>
                    <span style="font-size: 0.8rem; color: #6b7280;">{entry["timestamp"]}</span>
                </div>
                <p style="font-size: 0.9rem; margin: 0; color: #4b5563;">"{entry["text"][:40]}..."</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Add clear history button
        st.button("Clear History", key="clear_history", on_click=lambda: st.session_state.update({"emotion_history": []}))
        
        # Optional visualization of emotion over time
        if len(st.session_state.emotion_history) >= 3:
            st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
            st.markdown('<div class="card-header">Your Emotion Pattern</div>', unsafe_allow_html=True)
            
            # Prepare data for visualization
            history_df = pd.DataFrame(st.session_state.emotion_history)
            emotions_count = history_df['emotion'].value_counts().reset_index()
            emotions_count.columns = ['Emotion', 'Count']
            
            # Create pie chart
            fig = px.pie(emotions_count, values='Count', names='Emotion', 
                        color_discrete_sequence=px.colors.qualitative.Set3,
                        hole=0.4)
            fig.update_traces(
                textposition='inside', 
                textinfo='percent+label',
                marker=dict(line=dict(color='#FFFFFF', width=2))
            )
            fig.update_layout(
                margin=dict(l=20, r=20, t=20, b=20), 
                height=300,
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=-0.3,
                    xanchor="center",
                    x=0.5
                )
            )
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.markdown("""
        <div style="text-align: center; padding: 2rem 1rem;">
            <p style="color: #6b7280; font-size: 1rem;">No entries yet. Start by sharing how you feel!</p>
            <div style="font-size: 3rem; margin: 1rem 0;">📝</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Quick tips card
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-header">Quick Wellness Tips</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div style="padding: 0.75rem; border-radius: 8px; background-color: #f3f4f6; margin-bottom: 0.75rem;">
        <p style="margin: 0; font-size: 0.9rem;">🧘 Take 3 deep breaths when feeling overwhelmed</p>
    </div>
    <div style="padding: 0.75rem; border-radius: 8px; background-color: #f3f4f6; margin-bottom: 0.75rem;">
        <p style="margin: 0; font-size: 0.9rem;">💧 Stay hydrated throughout the day</p>
    </div>
    <div style="padding: 0.75rem; border-radius: 8px; background-color: #f3f4f6; margin-bottom: 0.75rem;">
        <p style="margin: 0; font-size: 0.9rem;">🚶‍♀️ A short walk can improve your mood</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("""
<div style="margin-top: 2rem; padding: 1rem; background-color: #f3f4f6; border-radius: 8px; text-align: center;">
    <p style="margin: 0; color: #6b7280; font-size: 0.9rem;">
        Track your emotions daily for better mental health awareness. 
        Remember that this tool is meant to complement, not replace, professional mental health care.
    </p>
</div>
""", unsafe_allow_html=True)