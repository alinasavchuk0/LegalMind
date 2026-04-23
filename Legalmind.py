import streamlit as st
import google.generativeai as genai
import time
import os
from dotenv import load_dotenv

load_dotenv()  # Ця команда завантажує ключ з файлу .env у пам'ять програми

# 1. Налаштування інтерфейсу
st.set_page_config(page_title="LegalMind 2.5 Final", page_icon="⚖️", layout="centered")

st.title("⚖️ LegalMind: Юридичний аналіз v2.5")
st.markdown("---")

# 2. Конфігурація API через змінні оточення
# Тепер ключ не "світиться" у коді, що захищає його від блокування
API_KEY = os.getenv("GOOGLE_API_KEY")

if API_KEY:
    genai.configure(api_key=API_KEY)
else:
    st.error("❌ API Ключ не знайдено! Переконайтеся, що ви налаштували змінні оточення.")

# 3. Функція аналізу (v2.5)
def ask_gemini(text):
    model = genai.GenerativeModel('gemini-2.5-flash')
    prompt = f"Ти — професійний юрист. Проаналізуй цей текст договору на ризики для орендаря: {text}"
    response = model.generate_content(prompt)
    return response.text

# 4. Інтерфейс користувача
user_input = st.text_area("Вставте текст договору:", height=200)

if st.button("🚀 ПУСК"):
    if not API_KEY:
        st.warning("Спочатку додайте API ключ у систему!")
    elif user_input:
        status_text = st.empty()
        status_text.info("⏳ З'єднання з сервером Gemini 2.5...")
        try:
            time.sleep(1)
            result = ask_gemini(user_input)
            status_text.empty()
            st.success("✅ Аналіз завершено!")
            st.markdown(result)
        except Exception as e:
            status_text.empty()
            st.error(f"Виникла помилка: {e}")
    else:
        st.warning("Будь ласка, введіть текст!")