import streamlit as st
import google.generativeai as genai
from gtts import gTTS
import io
import speech_recognition as sr
from streamlit_mic_recorder import mic_recorder
from langdetect import detect

# --- AYARLAR (ŞİFRENİ BURAYA GİR) ---
# Kendi aldığın AIza ile başlayan şifreyi tırnakların içine yapıştır.
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

# --- CSS TASARIM ---
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

# --- FONKSİYONLAR (SESLİ KONUŞMA VE ANLAMA) ---

def konus(metin):
    """Yapay zekanın cevabını sesli okur."""
    try:
        # Dili otomatik algıla
        try:
            algilanan_dil = detect(metin)
        except:
            algilanan_dil = 'tr' # Hata olursa Türkçe varsay
            
        # Kürtçe desteklenmiyorsa Türkçe motorunu kullan ama metni okumaya çalış
        dil_kodu = 'tr' 
        if algilanan_dil == 'ku':
            # Google TTS'de resmi Kürtçe desteği bazen kısıtlıdır, yine de deneriz
            dil_kodu = 'tr' 
        
        tts = gTTS(text=metin, lang=dil_kodu, slow=False)
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        fp.seek(0)
        # Sesi otomatik oynat
        st.audio(fp, format='audio/mp3', start_time=0)
    except Exception as e:
        st.warning(f"Ses çalamadım: {e}")

def sesi_yaziya_cevir(audio_bytes):
    """Mikrofondan gelen sesi yazıya çevirir."""
    r = sr.Recognizer()
    try:
        audio_data = sr.AudioData(audio_bytes, 16000, 2) 
        # Türkçe dinleme modu
        text = r.recognize_google(audio_data, language='tr-TR') 
        return text
    except sr.UnknownValueError:
        return None 
    except sr.RequestError:
        return None
    except Exception as e:
        return None

# --- ARAYÜZ BAŞLANGICI ---
st.markdown('<div class="baslik">BAKIL</div>', unsafe_allow_html=True)
st.caption("🚀 Sesli ve Zeki Asistan")

# --- SOHBET GEÇMİŞİ ---
if "messages" not in st.session_state:
    st.session_state.messages = []
    baslangic_mesaji = "Silav! Ez Bakıl im. Tu dikarî binivîsî an jî bi min re biaxivî. 🎙️"
    st.session_state.messages.append({"role": "assistant", "content": baslangic_mesaji})

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- KULLANICI GİRİŞİ ---

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

# --- YANIT İŞLEME ---
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
            message_placeholder.error(f"Hata oluştu: {e}")

# --- İMZA ---
st.markdown('<div class="alt-imza">DESIGNED BY HANİF TOPRAK</div>', unsafe_allow_html=True)
    .stChatMessage { background: rgba(255, 255, 255, 0.05); border-radius: 15px; margin-bottom: 10px; border: 1px solid rgba(255,255,255,0.1); }
    /* Mikrofon butonu ortalama */
    div[data-testid="stVerticalBlock"] > div:has(> div[data-testid="stMarkdownContainer"] > p:contains("🎙️")) {
        display: flex; justify-content: center;
    }
</style>
""", unsafe_allow_html=True)

# --- FONKSİYONLAR (SESLİ KONUŞMA VE ANLAMA) ---

def konus(metin):
    """Yapay zekanın cevabını sesli okur."""
    try:
        # Dili otomatik algıla (Türkçe mi Kürtçe mi?)
        algilanan_dil = detect(metin)
        # gTTS için dil kodunu ayarla (Kürtçe için 'ku', Türkçe için 'tr')
        dil_kodu = 'ku' if algilanan_dil == 'ku' else 'tr'
        
        tts = gTTS(text=metin, lang=dil_kodu, slow=False)
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        fp.seek(0)
        # Sesi otomatik oynat (autoplay)
        st.audio(fp, format='audio/mp3', start_time=0)
    except Exception as e:
        st.error(f"Ses hatası: {e}")

def sesi_yaziya_cevir(audio_bytes):
    """Mikrofondan gelen sesi yazıya çevirir."""
    r = sr.Recognizer()
    try:
        audio_data = sr.AudioData(audio_bytes, 16000, 2) # 16kHz, 2 byte width
        # Google'ın ücretsiz servisini kullan. Türkçe ağırlıklı dinle.
        text = r.recognize_google(audio_data, language='tr-TR') 
        return text
    except sr.UnknownValueError:
        return None # Ses anlaşılamadı
    except sr.RequestError:
        st.error("Ses servisine ulaşılamıyor.")
        return None
    except Exception as e:
        st.error(f"Hata: {e}")
        return None

# --- ARAYÜZ BAŞLANGICI ---
st.markdown('<div class="baslik">BAKIL</div>', unsafe_allow_html=True)
st.caption("🚀 Sesli ve Zeki Asistan")

# --- SOHBET GEÇMİŞİ ---
if "messages" not in st.session_state:
    st.session_state.messages = []
    # İlk açılış mesajı (sesli okumasın diye buraya eklemiyoruz, aşağıda özel işliyoruz)
    baslangic_mesaji = "Silav! Ez Bakıl im. Tu dikarî binivîsî an jî bi min re biaxivî. 🎙️"
    st.session_state.messages.append({"role": "assistant", "content": baslangic_mesaji})

# Geçmiş mesajları ekrana yaz
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- KULLANICI GİRİŞİ (MİKROFON VE KLAVYE) ---

# 1. Mikrofon Girişi
st.write("🎙️ Konuşmak için butona bas:")
audio = mic_recorder(start_prompt="Dinliyorum... (Kırmızı olunca konuş)", stop_prompt="Dinlemeyi Durdur", just_once=True, key='mic')

user_input = None

if audio:
    # Mikrofon kullanıldıysa sesi yazıya çevir
    st.spinner("Sesin yazıya çevriliyor...")
    mic_text = sesi_yaziya_cevir(audio['bytes'])
    if mic_text:
        user_input = mic_text
    else:
        st.warning("Sesini tam anlayamadım, tekrar dener misin?")

# 2. Klavye Girişi (Eğer mikrofon kullanılmadıysa)
if not user_input:
    user_input = st.chat_input("Buraya yazın...")

# --- YANIT İŞLEME ---
if user_input:
    # Kullanıcı mesajını ekrana bas
    st.chat_message("user").markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Yapay zeka yanıtı
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("Thinking...")
        try:
            # Gemini'ye sor
            response = model.generate_content(user_input)
            cevap_metni = response.text
            
            # Cevabı ekrana yaz
            message_placeholder.markdown(cevap_metni)
            st.session_state.messages.append({"role": "assistant", "content": cevap_metni})
            
            # --- SESLİ OKUMA (TTS) ---
            # Cevabı sesli olarak okut
            konus(cevap_metni)

        except Exception as e:
            message_placeholder.error(f"Bir hata oluştu: {e}")
            # Kotayı aşarsak yine hata verebilir, bu normaldir.

# --- İMZA ---
st.markdown('<div class="alt-imza">DESIGNED BY HANİF TOPRAK</div>', unsafe_allow_html=True)
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
</style>
""", unsafe_allow_html=True)

# --- BAŞLIK ---
st.markdown('<div class="baslik">BAKIL</div>', unsafe_allow_html=True)
st.caption("🚀 Asîstanê Te Yê Zîrek")

# --- ÖNERİ BUTONLARI (KÜRTÇE) ---
col1, col2, col3 = st.columns(3)
if col1.button("💡 Fikrekê Bide"):
    prompt = "Ji bo îro fikrekî cûda û xweş bide min."
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.spinner("Tê fikirîn..."):
        response = model.generate_content(prompt)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
        st.rerun()

if col2.button("📝 Helbest"):
    prompt = "Li ser welat û hêvîyê helbesteke kurt binivîse."
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.spinner("Tê nivîsandin..."):
        response = model.generate_content(prompt)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
        st.rerun()

if col3.button("🧠 Agahî"):
    prompt = "3 agahiyên balkêş û kurt bêje min."
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.spinner("Tê lêkolîn..."):
        response = model.generate_content(prompt)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
        st.rerun()


# --- SOHBET GEÇMİŞİ VE AÇILIŞ MESAJI ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Silav! Navê min Bakıl e. Ez çawa dikarim alîkariya te bikim?"}
    ]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- GİRİŞ KUTUSU ---
if prompt := st.chat_input("Li vir binivîse..."):
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        placeholder = st.empty()
        try:
            response = model.generate_content(prompt)
            placeholder.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except:
            placeholder.error("Pirsgirêka girêdanê.")

# --- İMZA ---
st.markdown('<div class="alt-imza">DESIGNED BY HANİF TOPRAK</div>', unsafe_allow_html=True)
