import streamlit as st
import sqlite3
from datetime import datetime
import openai
from anthropic import Anthropic
import google.generativeai as genai
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# --- DATABASE SETUP ---
# For Local: 'sqlite:///chat_history.db'
# For Cloud: Replace with your Postgres URL (e.g., 'postgresql://user:pass@host:5432/db')
DB_URL = "sqlite:///chat_history.db"
Base = declarative_base()

class ChatMessage(Base):
    __tablename__ = 'chat_history'
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    provider = Column(String(50))
    prompt = Column(Text)
    response = Column(Text)

engine = create_engine(DB_URL)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
db_session = Session()

# --- TEMPLATES ---
TEMPLATES = {
    "Short": {
        "Summarize": "Summarize the following text in 3 bullet points: ",
        "Grammar Fix": "Correct the grammar and spelling of this text: ",
        "Code Comment": "Add docstrings and comments to this Python code: ",
        "Translate (ES)": "Translate the following to Spanish: ",
        "Tone Checker": "Analyze the tone of this message: "
    },
    "Long": {
        "Blog Post": "Write a 500-word blog post about the following topic, including SEO keywords: ",
        "Technical Spec": "Create a detailed technical specification document for a software project based on these requirements: ",
        "Legal Disclaimer": "Draft a standard terms of service and privacy policy for a startup based on: ",
        "Curriculum Design": "Design a 4-week syllabus for a beginner course on: ",
        "Fiction Outline": "Create a chapter-by-chapter outline for a thriller novel featuring: "
    }
}

# --- UI CONFIGURATION ---
st.set_page_config(page_title="Universal AI Dashboard", layout="wide")
st.title("🤖 Universal AI Dashboard")

# --- SIDEBAR: API KEYS & MODEL SELECTION ---
with st.sidebar:
    st.header("Settings")
    provider = st.selectbox("Choose Provider", ["ChatGPT", "Claude", "Gemini"])
    
    api_key = st.text_input(f"Enter {provider} API Key", type="password")
    
    st.divider()
    st.subheader("Templates")
    t_type = st.radio("Template Length", ["Short", "Long"])
    selected_template = st.selectbox("Select Template", ["None"] + list(TEMPLATES[t_type].keys()))

# --- MAIN INTERFACE ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Template Logic
initial_value = ""
if selected_template != "None":
    initial_value = TEMPLATES[t_type][selected_template]

user_input = st.text_area("Your Request:", value=initial_value, height=200)

def call_llm(provider, prompt, key):
    if not key:
        return "Please provide an API key in the sidebar."
    
    try:
        if provider == "ChatGPT":
            client = openai.OpenAI(api_key=key)
            resp = client.chat.completions.create(
                model="gpt-4-turbo",
                messages=[{"role": "user", "content": prompt}]
            )
            return resp.choices[0].message.content
        
        elif provider == "Claude":
            client = Anthropic(api_key=key)
            resp = client.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=1024,
                messages=[{"role": "user", "content": prompt}]
            )
            return resp.content[0].text
        
        elif provider == "Gemini":
            genai.configure(api_key=key)
            model = genai.GenerativeModel('gemini-pro')
            resp = model.generate_content(prompt)
            return resp.text
            
    except Exception as e:
        return f"Error: {str(e)}"

if st.button("Send Request"):
    with st.spinner(f"Waiting for {provider}..."):
        response = call_llm(provider, user_input, api_key)
        
        # Save to Database
        new_msg = ChatMessage(provider=provider, prompt=user_input, response=response)
        db_session.add(new_msg)
        db_session.commit()
        
        st.subheader("Response")
        st.markdown(response)

# --- HISTORY SECTION ---
st.divider()
st.header("📜 Conversation History (Indefinite)")

history = db_session.query(ChatMessage).order_by(ChatMessage.timestamp.desc()).all()
for entry in history:
    with st.expander(f"{entry.timestamp.strftime('%Y-%m-%d %H:%M')} | {entry.provider}"):
        st.write(f"**Prompt:** {entry.prompt}")
        st.write(f"**Response:** {entry.response}")
