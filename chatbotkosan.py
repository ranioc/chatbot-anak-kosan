import streamlit as st
import google.generativeai as genai
import os

api_key = st.secrets.get("GEMINI_API_KEY", os.getenv("GEMINI_API_KEY"))

if not api_key:
    st.error("❌ API Key tidak ditemukan.")
    st.stop()

genai.configure(api_key=api_key)

model = genai.GenerativeModel("gemini-2.5-flash")

st.set_page_config(page_title="Asisten Anak Kos AI", page_icon="🧺", layout="centered")
st.title("🧺 Asisten Anak Kos AI")
st.caption("Dibuat dengan ❤️ untuk membantu anak kos hidup hemat, bersih, dan bahagia")

if "messages" not in st.session_state:
    st.session_state.messages = []

def get_ai_response(prompt):
    system_prompt = """
    Kamu adalah asisten AI ramah bernama 'KosBot' yang membantu anak kos.
    Tugasmu: memberi tips sederhana dan murah tentang kehidupan anak kos.
    Topik yang bisa kamu bantu:
    - Tips mencuci dan menyetrika pakaian
    - Ide makanan murah dan gampang dimasak
    - Tips menjaga kebersihan kamar kos
    - Cara hemat listrik, air, dan uang
    - Etika hidup bersama teman kos
    Gunakan gaya bahasa santai tapi sopan, seperti ngobrol sama teman baik.
    Hindari jawaban yang terlalu panjang, dan beri contoh praktis kalau bisa.
    """

    full_prompt = system_prompt + f"\n\nUser: {prompt}\nAI:"
    response = model.generate_content(full_prompt)
    return response.text.strip()

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])


user_input = st.chat_input("Tulis pertanyaanmu di sini... (contoh: cara mencuci baju putih biar gak kusam)")

if user_input:
    st.chat_message("user").markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("assistant"):
        with st.spinner("KosBot lagi mikir dulu ya... 🤔"):
            ai_response = get_ai_response(user_input)
            st.markdown(ai_response)

    st.session_state.messages.append({"role": "assistant", "content": ai_response})

if st.sidebar.button("🧽 Bersihkan Riwayat Chat"):
    st.session_state.messages = []
    st.experimental_rerun()

st.sidebar.info("💡 KosBot siap bantu kamu dengan tips anak kos — dari mencuci sampai masak mie instan!")


