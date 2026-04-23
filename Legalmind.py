import streamlit as st
import google.generativeai as genai
import time

# 1. Налаштування інтерфейсу (Етап 5 вашого проєкту)
st.set_page_config(page_title="LegalMind 2.5 Final", page_icon="⚖️", layout="centered")

st.title("⚖️ LegalMind: Юридичний аналіз v2.5")
st.markdown("---")

# 2. Конфігурація API
# Ваш робочий ключ
API_KEY = "AIzaSyCLFc0DO_SgfDQ3-JWpMrNyjdNQQDHJ5vM"
genai.configure(api_key=API_KEY)

# 3. Функція аналізу (та сама змінена функція)
def ask_gemini(text):
    # Використовуємо саме ту версію, яка у вас працює
    model = genai.GenerativeModel('gemini-2.5-flash')
    
    # Створюємо промпт (Етап 3: Промпт-інжиніринг)
    prompt = f"""
    Ти — професійний юрист. Проаналізуй цей текст договору:
    "{text}"
    
    Виділи головні ризики для орендаря та дай коротку пораду.
    Відповідай українською мовою.
    """
    
    response = model.generate_content(prompt)
    return response.text

# 4. Інтерфейс користувача
user_input = st.text_area("Вставте текст договору або пункт для аналізу:", height=200)

if st.button("🚀 ПУСК"):
    if user_input:
        # Створюємо контейнер для статусу, щоб користувач бачив процес
        status_text = st.empty()
        status_text.info("⏳ З'єднання з сервером Google Gemini 2.5...")
        
        try:
            # Невелика технічна пауза для стабільності
            time.sleep(1)
            
            # Виклик функції
            result = ask_gemini(user_input)
            
            # Прибираємо статус завантаження і показуємо результат
            status_text.empty()
            st.success("✅ Аналіз завершено успішно!")
            
            st.subheader("🔍 Висновок ШІ-юриста:")
            st.markdown(result)
            
        except Exception as e:
            status_text.empty()
            error_str = str(e)
            
            if "429" in error_str:
                st.error("🛑 Помилка квоти: Сервери Google просять зачекати. Спробуйте натиснути ще раз через 30-60 секунд.")
            elif "404" in error_str:
                st.error("❌ Модель не знайдена. Спробуйте змінити версію в коді на 'gemini-1.5-flash'.")
            else:
                st.error(f"Виникла технічна помилка: {error_str}")
    else:
        st.warning("Будь ласка, введіть текст для аналізу!")

# Футер
st.markdown("---")
st.caption("LegalMind AI | Версія 2.5 (Experimental Access)")