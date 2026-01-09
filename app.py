import streamlit as st
import google.generativeai as genai
from gtts import gTTS
import io
import speech_recognition as sr
from streamlit_mic_recorder import mic_recorder
from langdetect import detect

# --- AYARLAR ---
# Senin API Anahtarın (Ücretsiz Gemini Pro Anahtarı)
SIFRE = "AIzaSyBVPm17FHeyGFqu_dUuWcz6oXwdb-3sOq4"
genai.configure(api_key=SIFRE)

# --- PLAN B: MODEL AYARI (Gemini Pro) ---
# Bu model en eski ve en sağlam modeldir. Her sürümde çalışır. ÜCRETSİZDİR.
try:
    model = genai.GenerativeModel('gemini-pro')
except:
    # Eğer pro da hata verirse, en temel modeli dener
    model = genai.GenerativeModel('gemini-1.0-pro')

# --- GİZLİ KİMLİK ---
GIZLI_KIMLIK = """
Senin adın Bakıl. 
Sen Kürtçe ve Türkçe bilen, çok zeki, yardımsever ve Kürdistanlı bir asistansın.
Geliştiricin: HANİF TOPRAK.
Eğer biri sana "Nerelisin?" derse kesinlikle "Kürdistanlıyım" de.
Cevapların kısa, net ve samimi olsun.
"""

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="Bakıl AI", page_icon="🦁", layout="centered", initial_sidebar_state="collapsed")

# --- CSS TASARIM ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;600&display=swap');

.stApp { 
    background: linear-gradient(-45deg, #0f0c29, #302b63, #24243e); 
    background-size: 400% 400%; 
    font-family: 'Montserrat', sans-serif; 
    color: white; 
}

header, footer, #MainMenu {visibility: hidden;}

.baslik { 
    font-size: 50px; 
    font-weight: 600; 
    text-align: center; 
    color: #fcf6ba;
    margin-bottom: 10px; 
    text-shadow: 0px 0px 10px rgba(255, 215, 0, 0.3); 
}

.alt-imza { 
    position: fixed; 
    bottom: 10px; 
    left: 0; 
    width: 100%; 
    text-align: center; 
    font-size: 10px; 
    color: rgba(255,255,255,0.3); 
    letter-spacing: 3px; 
    z-index: 99; 
    pointer-events: none; 
}

.stChatMessage { 
    background: rgba(255, 255, 255, 0.05); 
    border-radius: 15px; 
    margin-bottom: 10px; 
    border: 1px solid rgba(255,255,255,0.1); 
}

div[data-testid="stVerticalBlock"] > div:has(> div[data-testid="stMarkdownContainer"] > p:contains("🎙️")) {
    display: flex; 
    justify-content: center; 
}
</style>
""", unsafe_allow_html=True)

# --- FONKSİYONLAR ---

def konus(metin):
    try:
        # Basit Türkçe okuma (En garanti yöntem)
        tts = gTTS(text=metin, lang='tr', slow=False)
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        fp.seek(0)
        st.audio(fp, format='audio/mp3', start_time=0)
    except:
        pass

def sesi_yaziya_cevir(audio_bytes):
    r = sr.Recognizer()
    try:
        audio_data = sr.AudioData(audio_bytes, 16000, 2) 
        text = r.recognize_google(audio_data, language='tr-TR') 
        return text
    except:
        return None

# --- ARAYÜZ ---
st.markdown('<div class="baslik">BAKIL</div>', unsafe_allow_html=True)
st.caption("🚀 Sesli ve Zeki Asistan (Pro Modu)")

if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages.append({"role": "assistant", "content": "Silav! Ez Bakıl im. Tu dikarî binivîsî an jî bi min re biaxivî. 🎙️"})

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

st.write("🎙️ Konuşmak için butona bas:")
audio = mic_recorder(start_prompt="Dinliyorum... (Bas)", stop_prompt="Dur (Tamam)", just_once=True, key='mic')

user_input = None

if audio:
    st.spinner("Sesin yazıya çevriliyor...")
    mic_text = sesi_yaziya_cevir(audio['bytes'])
    if mic_text:
        user_input = mic_text

if not user_input:
    user_input = st.chat_input("Buraya yazın...")

if user_input:
    st.chat_message("user").markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("Thinking...")
        try:
            tam_prompt = GIZLI_KIMLIK + "\n\nKullanıcı dedi ki: " + user_input
            response = model.generate_content(tam_prompt)
            cevap_metni = response.text
            
            message_placeholder.markdown(cevap_metni)
            st.session_state.messages.append({"role": "assistant", "content": cevap_metni})
            konus(cevap_metni)

        except Exception as e:
            message_placeholder.error(f"Hata: {e}")

st.markdown('<div class="alt-imza">DESIGNED BY HANİF TOPRAK</div>', unsafe_allow_html=True)
                   
