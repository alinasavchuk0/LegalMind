import streamlit as st
import google.generativeai as genai
import os
import time
from dotenv import load_dotenv

# 1. Налаштування сторінки
st.set_page_config(page_title="LegalMind Premium", page_icon="⚖️", layout="centered")

# 2. Кастомний CSS
st.markdown("""
    <style>
    /* Головний фон з хаотичними лініями */
    .stApp {
        background-color: #E5D3B3;
        background-image: 
            linear-gradient(110deg, transparent 40%, rgba(112, 28, 28, 0.04) 41%, transparent 42%),
            linear-gradient(200deg, transparent 70%, rgba(112, 28, 28, 0.04) 71%, transparent 72%),
            radial-gradient(at 10% 10%, rgba(112, 28, 28, 0.03) 0px, transparent 50%);
        background-attachment: fixed;
    }
    
    /* ТЕКСТ В ПЕРЕВІРЦІ - ЧОРНИЙ */
    .stTextArea textarea {
        color: #000000 !important;
        -webkit-text-fill-color: #000000 !important;
        background-color: #ffffff !important;
        border: 1px solid #701C1C !important;
        border-radius: 5px;
        font-size: 16px;
    }

    /* ЗАГОЛОВОК */
    h1 {
        color: #701C1C; 
        font-family: 'Playfair Display', serif;
        font-weight: 800;
        text-align: center;
        text-transform: uppercase;
        letter-spacing: 3px;
    }

    /* КНОПКИ */
    .stButton>button {
        background-color: #701C1C;
        color: #D4AF37 !important;
        border: 1px solid #D4AF37;
        width: 100%;
    }
    
    .stButton>button:hover {
        background-color: #D4AF37;
        color: #701C1C !important;
    }

    /* КАРТКА ВЕРДИКТУ - ТОЧНА ШИРИНА */
    .report-card {
        background: #ffffff;
        padding: 25px;
        border: 1px solid #701C1C;
        color: #000000;
        font-family: 'Georgia', serif;
        width: 100%;
        margin-top: 15px;
        display: block;
    }

    .gold-line {
        height: 2px;
        background: linear-gradient(90deg, transparent, #701C1C, transparent);
        margin: 20px 0;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Логіка API
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
if api_key:
    genai.configure(api_key=api_key)

def ask_gemini(text):
    model = genai.GenerativeModel('gemini-2.5-flash')
    prompt = f"Ти елітний корпоративний юрист. Проаналізуй цей текст на ризики, структуруй відповідь: {text}"
    response = model.generate_content(prompt)
    return response.text

# 4. Інтерфейс
st.title("LEGALMIND AI")
st.markdown('<div class="gold-line"></div>', unsafe_allow_html=True)

# Session state для очищення
if 'text_val' not in st.session_state:
    st.session_state.text_val = ""

# Використовуємо контейнер для фіксації ширини
with st.container():
    u_input = st.text_area("DOCUMENT", 
                           value=st.session_state.text_val, 
                           height=250, 
                           key="main_input",
                           label_visibility="collapsed")

    col1, col2 = st.columns([3, 1])
    with col1:
        btn_run = st.button("⚖️ EXECUTE LEGAL AUDIT")
    with col2:
        if st.button("🗑️ RESET"):
            st.session_state.text_val = ""
            st.rerun()

    # Вивід результату ТУТ ЖЕ всередині контейнера
    if btn_run:
        if u_input:
            with st.spinner('CONSULTING...'):
                try:
                    result = ask_gemini(u_input)
                    st.markdown(f"""
                        <div class="report-card">
                            <h2 style="color: #701C1C; margin:0;">LEGAL VERDICT</h2>
                            <hr style="border: 0.5px solid #D4AF37; margin: 15px 0;">
                            <div style="color: #000000; line-height: 1.6;">
                                {result.replace('\\n', '<br>')}
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"SYSTEM ERROR: {e}")
        else:
            st.warning("PLEASE PROVIDE TEXT.")

st.markdown('<br><div class="gold-line"></div>', unsafe_allow_html=True)
st.caption("ESTABLISHED 2026 | PREMIUM LEGAL TECH")