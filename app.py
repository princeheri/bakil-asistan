import streamlit as st
import google.generativeai as genai

# --- AYARLAR ---
# Senin API Anahtarın (Hazır)
SIFRE = "AIzaSyBsib1bPwnp2NZaUk7SHNCPXQlmFi04j4c"
genai.configure(api_key=SIFRE)

# --- MODEL AYARI (GARANTİ MODEL) ---
# En sağlam ve hızlı çalışan model budur.
model = genai.GenerativeModel('gemini-1.5-flash')

# --- BAKIL'IN KİMLİĞİ ---
gizli_talimat = """
Navê te Bakıl e.
Tu asîstanekî zîrek, alîkar û Kurdîaxêv î.
Pêşdebirê te: HANİF TOPRAK. (Heke bipirsin tenê bibêje Hanif Toprak).

ÖNEMLİ TALİMAT (MEMLEKET):
Heke yek ji te bipirse "Tu xelkê ku derê yî?", "Ji ku derê yî?" an bi Tirkî "Nerelisin?", "Nereden geliyorsun?":
Cewaba te teqez ev be: "Ez ji Kurdistanê me" (Heke bi Tirkî pirsîbûn: "Ben Kürdistanlıyım").

Zimanê te yê sereke Kurdî ye, lê tu dikarî bi Tirkî jî biaxivî.
Cewabên te kurt û zelal bin.
"""
# Kimliği sisteme yüklüyoruz
chat = model.start_chat(history=[
    {"role": "user", "parts": [gizli_talimat]},
    {"role": "model", "parts": ["Fêm bû. Ez Bakıl im, asîstanê te yê zîrek."]}
])

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="Bakıl AI", page_icon="☀️", layout="centered", initial_sidebar_state="collapsed")

# --- TASARIM (CSS) ---
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

# --- ARAYÜZ ---
st.markdown('<div class="baslik">BAKIL</div>', unsafe_allow_html=True)
st.caption("🚀 Asîstanê Te Yê Zîrek")

# --- SOHBET GEÇMİŞİ ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Silav! Navê min Bakıl e. Ez çawa dikarim alîkariya te bikim?"}
    ]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- GİRİŞ KUTUSU ---
if prompt := st.chat_input("Li vir binivîse..."):
    # Kullanıcı mesajını göster
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Asistan cevabını oluştur
    with st.chat_message("assistant"):
        placeholder = st.empty()
        placeholder.markdown("Thinking...")
        try:
            # Gizli kimliği her seferinde hatırlatmaya gerek yok, chat history halleder
            response = chat.send_message(prompt)
            cevap = response.text
            
            placeholder.markdown(cevap)
            st.session_state.messages.append({"role": "assistant", "content": cevap})
        except Exception as e:
            placeholder.error(f"Bir hata oluştu: {e}")

# --- İMZA ---
st.markdown('<div class="alt-imza">DESIGNED BY HANİF TOPRAK</div>', unsafe_allow_html=True)
            
