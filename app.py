import streamlit as st
import google.generativeai as genai
from gtts import gTTS
import io
import speech_recognition as sr
from streamlit_mic_recorder import mic_recorder
from langdetect import detect

# --- AYARLAR (SENİN GÖNDERDİĞİN ŞİFRE EKLENDİ) ---
SIFRE = "AIzaSyBVPm17FHeyGFqu_dUuWcz6oXwdb-3sOq4"
genai.configure(api_key=SIFRE)

# --- YAPAY ZEKANIN KİMLİĞİ ---
gizli_talimat = """
Navê te Bakıl e.
Tu asîstanekî zîrek, alîkar û Kurdîaxêv î.
Pêşdebirê te: HANİF TOPRAK.
Heke yek ji te bipirse "Tu xelkê ku derê yî?", cewaba te teqez ev be: "Ez ji Kurdistanê me".
Zimanê te yê sereke Kurdî ye, lê tu dikarî bi Tirkî jî biaxivî.
Cevapların kısa, öz ve net olsun.
"""
model = genai.GenerativeModel('gemini-1.5-flash', system_instruction=gizli_talimat)

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="Bakıl AI", page_icon="🦁", layout="centered", initial_sidebar_state="collapsed")

# --- CSS TASARIM (HATA VERMEMESİ İÇİN SOLA YAPIŞIK) ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;600&display=swap');

@keyframes gradient { 
    0% {background-position: 0% 50%;} 
    50% {background-position: 100% 50%;} 
    100% {background-position: 0% 50%;} 
}

.stApp { 
    background: linear-gradient(-45deg, #0f0c29, #302b63, #24243e); 
    background-size: 400% 400%; 
    animation: gradient 15s ease infinite; 
    font-family: 'Montserrat', sans-serif; 
    color: white; 
}

header, footer, #MainMenu {visibility: hidden;}

.baslik { 
    font-size: 50px; 
    font-weight: 600; 
    text-align: center; 
    background: linear-gradient(to right, #bf953f, #fcf6ba, #b38728, #fbf5b7, #aa771c); 
    -webkit-background-clip: text; 
    -webkit-text-fill-color: transparent; 
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

/* Mikrofon butonu ortalama */
div[data-testid="stVerticalBlock"] > div:has(> div[data-testid="stMarkdownContainer"] > p:contains("🎙️")) {
    display: flex; 
    justify-content: center; 
}
</style>
""", unsafe_allow_html=True)

# --- FONKSİYONLAR ---

def konus(metin):
    try:
        try:
            algilanan_dil = detect(metin)
        except:
            algilanan_dil = 'tr'
            
        dil_kodu = 'tr' 
        if algilanan_dil == 'ku':
            dil_kodu = 'tr' 
        
        tts = gTTS(text=metin, lang=dil_kodu, slow=False)
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        fp.seek(0)
        st.audio(fp, format='audio/mp3', start_time=0)
    except Exception as e:
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
st.caption("🚀 Sesli ve Zeki Asistan")

if "messages" not in st.session_state:
    st.session_state.messages = []
    baslangic_mesaji = "Silav! Ez Bakıl im. Tu dikarî binivîsî an jî bi min re biaxivî. 🎙️"
    st.session_state.messages.append({"role": "assistant", "content": baslangic_mesaji})

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
    else:
        st.warning("Sesini tam anlayamadım, tekrar dener misin?")

if not user_input:
    user_input = st.chat_input("Buraya yazın...")

if user_input:
    st.chat_message("user").markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("Thinking...")
        try:
            response = model.generate_content(user_input)
            cevap_metni = response.text
            
            message_placeholder.markdown(cevap_metni)
            st.session_state.messages.append({"role": "assistant", "content": cevap_metni})
            
            konus(cevap_metni)

        except Exception as e:
            message_placeholder.error(f"Hata: {e}")

st.markdown('<div class="alt-imza">DESIGNED BY HANİF TOPRAK</div>', unsafe_allow_html=True)
