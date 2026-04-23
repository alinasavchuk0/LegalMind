import streamlit as st
import google.generativeai as genai
import os
import time
from dotenv import load_dotenv
from PyPDF2 import PdfReader

# 1. Налаштування сторінки
st.set_page_config(page_title="LegalMind Ultra", page_icon="⚖️", layout="centered")

# 2. Кастомний CSS (Дизайн + Текст)
st.markdown("""
    <style>
    .stApp {
        background-color: #E5D3B3;
        background-image: 
            linear-gradient(110deg, transparent 40%, rgba(112, 28, 28, 0.04) 41%, transparent 42%),
            linear-gradient(200deg, transparent 70%, rgba(112, 28, 28, 0.04) 71%, transparent 72%);
        background-attachment: fixed;
    }
    
    /* Текст у полях - ЧОРНИЙ */
    .stTextArea textarea, .stTextInput input {
        color: #000000 !important;
        background-color: #ffffff !important;
    }

    h1, h2, h3 {
        color: #701C1C;
        font-family: 'Playfair Display', serif;
        text-align: center;
    }

    /* Кнопки */
    .stButton>button {
        background-color: #701C1C;
        color: #D4AF37 !important;
        border: 1px solid #D4AF37;
        width: 100%;
        border-radius: 5px;
    }

    /* Картка результату */
    .report-card {
        background: #ffffff;
        padding: 20px;
        border: 1px solid #701C1C;
        color: #000000;
        border-radius: 5px;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Допоміжні функції
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
if api_key:
    genai.configure(api_key=api_key)

def extract_text_from_pdf(file):
    pdf_reader = PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

def ask_gemini(text, prompt_type):
    model = genai.GenerativeModel('gemini-2.5-flash')
    full_prompt = f"Ти професійний юрист. Проаналізуй цей текст: {text}. Надай {prompt_type}."
    response = model.generate_content(full_prompt)
    return response.text

# 4. Інтерфейс
st.title("LEGALMIND ULTRA AI")
st.markdown("<center>Преміальний юридичний аудит документів</center>", unsafe_allow_html=True)

# Бічна панель
with st.sidebar:
    st.header("⚙️ НАЛАШТУВАННЯ")
    doc_type = st.selectbox("Тип документа", ["Договір оренди", "Трудовий договір", "Контракт купівлі-продажу", "Інше"])
    st.info("Виберіть тип для більш точного аналізу")

# Вибір способу введення
input_mode = st.radio("Спосіб подачі документа:", ["Вставити текст", "Завантажити PDF"], horizontal=True)

final_text = ""

if input_mode == "Вставити текст":
    final_text = st.text_area("ВСТАВТЕ ТЕКСТ", height=200, placeholder="Скопіюйте сюди пункти договору...", key="manual_text")
else:
    uploaded_file = st.file_uploader("ЗАВАНТАЖТЕ PDF ФАЙЛ", type="pdf")
    if uploaded_file:
        with st.spinner("Зчитуємо PDF..."):
            final_text = extract_text_from_pdf(uploaded_file)
            st.success("Текст із PDF успішно вилучено!")

# Кнопки управління
col1, col2 = st.columns([3, 1])
with col1:
    execute = st.button("⚖️ ЗАПУСТИТИ ПОВНИЙ АУДИТ")
with col2:
    if st.button("🗑️ СИНХРОНІЗАЦІЯ"):
        st.rerun()

# 5. ЛОГІКА АНАЛІЗУ
if execute:
    if not final_text:
        st.warning("Спочатку додайте текст або файл!")
    else:
        with st.spinner("ШІ проводить глибокий аналіз..."):
            try:
                # Отримуємо різні частини аналізу паралельно (або послідовно)
                risks = ask_gemini(final_text, "перелік критичних ризиків для клієнта")
                advice = ask_gemini(final_text, "юридичні поради щодо покращення позиції")
                score_raw = ask_gemini(final_text, "оцінку ризику від 1 до 100 одним числом")
                
                # Візуалізація шкали ризику
                try:
                    score = int(''.join(filter(str.isdigit, score_raw[:4])))
                except:
                    score = 50
                
                st.subheader("📊 РІВЕНЬ ЮРИДИЧНОЇ НЕБЕЗПЕКИ")
                color = "green" if score < 30 else "orange" if score < 70 else "red"
                st.markdown(f"<h1 style='color:{color}; font-size: 50px;'>{score}%</h1>", unsafe_allow_html=True)
                st.progress(score / 100)

                # Вкладки з результатом
                tab1, tab2, tab3 = st.tabs(["🔍 КРИТИЧНІ РИЗИКИ", "💡 ПОРАДИ ЮРИСТА", "📄 ПОВНИЙ ТЕКСТ"])
                
                with tab1:
                    st.markdown(f'<div class="report-card">{risks}</div>', unsafe_allow_html=True)
                
                with tab2:
                    st.markdown(f'<div class="report-card">{advice}</div>', unsafe_allow_html=True)
                
                with tab3:
                    st.text_area("Зчитаний текст:", final_text, height=300)
                
                # Кнопка завантаження (імітація)
                st.download_button("📥 ЗАВАНТАЖИТИ ЗВІТ (TXT)", data=f"РИЗИКИ:\n{risks}\n\nПОРАДИ:\n{advice}", file_name="Legal_Verdict.txt")

            except Exception as e:
                st.error(f"Помилка аналізу: {e}")

st.caption("© 2026 LegalMind Ultra | Premium Corporate Solutions")